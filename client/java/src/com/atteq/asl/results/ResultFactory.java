package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

public interface ResultFactory<T, R extends Result<T>> {

	public R create(Performer performer, T result);

}
