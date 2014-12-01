package com.atteq.asl;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.Result;
import com.atteq.asl.results.ResultTransformer;

public interface AtteqServiceLayer {

	public <T, R extends Result<T>> R perform(Performer performer, ResultTransformer<T, R> resultTransformer)
			throws ServiceCallException;

}