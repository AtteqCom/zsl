package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import org.apache.log4j.Logger;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;

public class JsonResultTransformer<T, R extends Result<T>> implements ResultTransformer<T, R> {

	protected ResultFactory<T, R> factory;

	Logger logger = Logger.getLogger(getClass());

	public JsonResultTransformer(ResultFactory<T, R> factory) {
		this.factory = factory;
	}

	@Override
	public R transform(Performer performer, String result, int status, JavaType type) throws TransformationException {
		ObjectMapper mapper = new ObjectMapper();
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		try {
			logger.debug(String.format("Response:\n%s", result));
			T r = mapper.readValue(result, type);
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
