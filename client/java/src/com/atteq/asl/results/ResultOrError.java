package com.atteq.asl.results;

public class ResultOrError<ResultType, ErrorType extends Error>  {

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
		return result;
	}

	public ErrorType getError() {
		return error;
	}

}
