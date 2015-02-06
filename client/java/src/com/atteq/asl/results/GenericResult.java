package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

/**
 * Generic result - contains a result object in {@code result} property and the
 * performer which generated the result - {@code performer} property.
 *
 * @author Martin Babka
 *
 * @param <T> Type of the result.
 */
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
