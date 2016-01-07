package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;
import com.fasterxml.jackson.databind.JavaType;

/**
 * An infrastructure for creating results from raw responses.
 *
 * @author Martin Babka
 *
 * @param <T>
 *            Type of the result - usually POJO returned in the response.
 * @param <R>
 *            Type of the result holder - implements {@see Result} interface.
 */
public interface ResultTransformer<T, R extends Result<T>> {

	/**
	 * Transforms the raw result info a nice structure implementing
	 * {@see Result} interface.
	 *
	 * @param performer
	 *            Performer which generated the data.
	 * @param result
	 *            Raw result - string.
	 * @param status
	 *            Response status.
	 * @param type
	 *            Type descriptor of the result {@code T} type. Used by JSON
	 *            mapper.
	 * @return The nice result.
	 * @throws TransformationException
	 *             If JSON mapping fails.
	 */
	public R transform(Performer performer, String result, int status, JavaType type) throws TransformationException;

}
