package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

/**
 * Factory which creates result objects - {@link ResultFactory.create} is just a
 * constructor for a suitable object implementing {@link Result} interface.
 *
 * @author Martin Babka
 *
 * @param <T>
 *            Type of the object.
 * @param <R>
 *            Result object - holds both performer and the plain result of type
 *            {@code T}.
 */
public interface ResultFactory<T, R extends Result<T>> {

	/**
	 * Create method.
	 *
	 * @param performer
	 *            Performer.
	 * @param result
	 *            Plain result.
	 * @return Compound result.
	 */
	public R create(Performer performer, T result);

}
