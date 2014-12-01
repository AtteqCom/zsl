package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

public class GenericResult<T> implements Result<T> {

	private final Performer performer;

	private final T result;

	public GenericResult(Performer performer, T result) {
		this.performer = performer;
		this.result = result;
	}

	@Override
	public Performer getPerformer() {
		return performer;
	}

	@Override
	public T getResult() {
		return result;
	}

}
