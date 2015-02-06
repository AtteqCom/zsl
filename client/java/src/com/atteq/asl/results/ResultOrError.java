package com.atteq.asl.results;

/**
 * Plain result object for responses which can be either a valid result or an
 * error description.
 *
 * @author Martin Babka
 *
 * @param <ResultType>
 *            Result type.
 * @param <ErrorType>
 *            Error type.
 */
public class ResultOrError<ResultType, ErrorType extends Error> {

	final ResultType result;
	final ErrorType error;
	final boolean errorFlag;

	public ResultOrError(boolean errorFlag, ResultType result, ErrorType error) {
		this.errorFlag = errorFlag;
		this.error = error;
		this.result = result;
	}

	public ResultOrError(ResultType result) {
		this.errorFlag = false;
		this.error = null;
		this.result = result;
	}

	public ResultOrError(ErrorType error) {
		this.errorFlag = true;
		this.error = error;
		this.result = null;
	}

	public boolean isError() {
		return errorFlag;
	}

	public ResultType getResult() {
		if (isError()) {
			throw new java.lang.Error("Can not access result on error.");
		}
		return result;
	}

	public ErrorType getError() {
		if (!isError()) {
			throw new java.lang.Error("Can not access error data on success.");
		}
		return error;
	}

}
