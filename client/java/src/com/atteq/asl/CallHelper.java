package com.atteq.asl;

import com.atteq.asl.performers.Performer;
import com.atteq.asl.results.GenericResult;
import com.atteq.asl.results.GenericResultFactory;
import com.atteq.asl.results.JsonResultTransformer;
import com.atteq.asl.tasks.JsonResultWithErrorTransformer;
import com.atteq.asl.tasks.Task;
import com.atteq.asl.tasks.TaskResult;
import com.atteq.asl.tasks.TaskResultFactory;
import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.type.TypeFactory;

public abstract class CallHelper {

	public static <T> TaskResult<T> perform(AtteqServiceLayer asl, Task task, JavaType t) throws ServiceCallException {
		TaskResultFactory<T> f = new TaskResultFactory<T>();
		return asl.perform(task, new JsonResultTransformer<T, TaskResult<T>>(f), t);
	}

	public static <T> TaskResult<T> perform(AtteqServiceLayer asl, Task task, Class<T> c) throws ServiceCallException {
		TaskResultFactory<T> f = new TaskResultFactory<T>();
		return asl.perform(task, new JsonResultTransformer<T, TaskResult<T>>(f),
				TypeFactory.defaultInstance().constructType(c));
	}

	public static <T> TaskResult<T> performWithErrorDecorator(AtteqServiceLayer asl, Task task, JavaType t)
			throws ServiceCallException {
		return asl.perform(task, new JsonResultWithErrorTransformer<T>(), t);
	}

	public static <T> TaskResult<T> performWithErrorDecorator(AtteqServiceLayer asl, Task task, Class<T> c)
			throws ServiceCallException {
		return asl.perform(task, new JsonResultWithErrorTransformer<T>(),
				TypeFactory.defaultInstance().constructType(c));
	}

	public static <T> GenericResult<T> perform(AtteqServiceLayer asl, Performer performer, JavaType t)
			throws ServiceCallException {
		GenericResultFactory<T> f = new GenericResultFactory<T>();
		return asl.perform(performer, new JsonResultTransformer<T, GenericResult<T>>(f), t);
	}

	public static <T> GenericResult<T> perform(AtteqServiceLayer asl, Performer performer, Class<T> c)
			throws ServiceCallException {
		GenericResultFactory<T> f = new GenericResultFactory<T>();
		return asl.perform(performer, new JsonResultTransformer<T, GenericResult<T>>(f),
				TypeFactory.defaultInstance().constructType(c));
	}

}
