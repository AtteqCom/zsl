package com.atteq.asl.tasks;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.ResultFactory;

public class TaskResultFactory<T> implements ResultFactory<T, TaskResult<T>> {

	@Override
	public TaskResult<T> create(Performer performer, T result) {
		return new TaskResult<T>((Task) performer, result);
	}

}
