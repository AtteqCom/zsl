package com.atteq.asl.tasks;

public class TaskResultWithError<T> extends TaskResult<T> {

	private final String error;

	public TaskResultWithError(Task task, T result) {
		super(task, result);
		error = null;
	}

	public TaskResultWithError(Task task, String error) {
		super(task, null);
		this.error = error;
	}

	public boolean isError() {
		return error != null;
	}

	public String getError() {
		return error;
	}

}
