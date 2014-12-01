package com.atteq.asl.tasks;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.GenericResult;
import com.atteq.asl.results.GenericResultFactory;
import com.atteq.asl.results.JsonResultTransformer;
import com.atteq.asl.results.ResultTransformer;
import com.atteq.asl.results.TransformationException;

public class JsonResultWithErrorTransformer<T> implements ResultTransformer<T, TaskResultWithError<T>> {

	public static class ResultWithError {

		public String data;

		public String error;

	}

	@Override
	public TaskResultWithError<T> transform(Performer performer, String result, int status)
			throws TransformationException {
		GenericResultFactory<ResultWithError> f1 = GenericResultFactory.getInstance();
		ResultTransformer<ResultWithError, GenericResult<ResultWithError>> rt1;
		rt1 = new JsonResultTransformer<ResultWithError, GenericResult<ResultWithError>>(f1);

		ResultWithError rwe = rt1.transform(performer, result, status).getResult();

		if (rwe.error != null) {
			return new TaskResultWithError<T>((Task) performer, rwe.error);
		} else {
			GenericResultFactory<T> f2 = GenericResultFactory.getInstance();
			ResultTransformer<T, GenericResult<T>> rt2;
			rt2 = new JsonResultTransformer<T, GenericResult<T>>(f2);
			T res = rt2.transform(performer, rwe.data, status).getResult();
			return new TaskResultWithError<T>((Task) performer, res);
		}
	}
}
