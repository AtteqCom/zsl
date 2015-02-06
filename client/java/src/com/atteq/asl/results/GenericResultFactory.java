package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

/**
 * Factory for creating GenericResult. See {@link ResultFactory} for the concept.
 *
 * @author Martin Babka
 *
 * @param <T> Type of the result object.
 */
public class GenericResultFactory<T> implements ResultFactory<T, GenericResult<T>> {

	public GenericResult<T> create(Performer performer, T result) {
		return new GenericResult<T>(performer, result);
	}

	public static <T> GenericResultFactory<T> getInstance() {
		return new GenericResultFactory<T>();
	}

}