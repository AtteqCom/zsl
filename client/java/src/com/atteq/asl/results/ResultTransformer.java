package com.atteq.asl.results;

import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;

public interface ResultTransformer<T, R extends Result<T>> {

	public R transform(Performer performer, String result, int status, JavaType type) throws TransformationException;

}
