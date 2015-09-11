package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.tasks.Task;
import com.atteq.asl.tasks.TaskResultWithError;
import com.atteq.asl.utils.JsonHelper;

public class JsonResultWithErrorTransformer<T> implements ResultTransformer<T, TaskResultWithError<T>> {

	protected ObjectMapper mapper = JsonHelper.createMapper();

	public static class Result {

		String data;
		String error;

		public String getData() {
			return data;
		}

		public void setData(String data) {
			this.data = data;
		}

		public String getError() {
			return error;
		}

		public void setError(String error) {
			this.error = error;
		}

	}

	@SuppressWarnings("unchecked")
	@Override
	public TaskResultWithError<T> transform(Performer performer, String result, int status, JavaType type)
			throws TransformationException {

		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		try {
			Result r = mapper.readValue(result, Result.class);
			return r.getError() == null
					? new TaskResultWithError<T>((Task) performer, (T) mapper.readValue(r.getData(), type))
					: new TaskResultWithError<T>((Task) performer, r.getError());
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

	public JavaType getType(Class<T> cls) {
		return mapper.getTypeFactory().constructType(cls);
	}
}
