package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

public interface ResultTransformer<T, R extends Result<T>> {

	public R transform(Performer performer, String result, int status) throws TransformationException;

}
