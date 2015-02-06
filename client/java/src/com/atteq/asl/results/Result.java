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
public interface Result<T> {

	public Performer getPerformer();

	public T getResult();

}
