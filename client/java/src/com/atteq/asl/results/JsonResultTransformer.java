package com.atteq.asl.results;

import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.utils.JsonHelper;

public class JsonResultTransformer<T, R extends Result<T>> implements ResultTransformer<T, R> {

	protected ResultFactory<T, R> factory;

	public JsonResultTransformer(ResultFactory<T, R> factory) {
		this.factory = factory;
	}

	@Override
	public R transform(Performer performer, String result, int status, JavaType type) throws TransformationException {
		try {
			T r = JsonHelper.createMapper().readValue(result, type);
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
