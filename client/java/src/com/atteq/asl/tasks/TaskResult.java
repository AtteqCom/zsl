package com.atteq.asl.tasks;

import com.atteq.asl.results.GenericResult;

public class TaskResult<T> extends GenericResult<T> {

	public TaskResult(Task task, T result) {
		super(task, result);
	}

	public Task getTask() {
		return getPerformer();
	}

	@Override
	public Task getPerformer() {
		return (Task) super.getPerformer();
	}

}
