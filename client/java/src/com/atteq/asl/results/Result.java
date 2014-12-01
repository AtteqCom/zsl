package com.atteq.asl.results;

import com.atteq.asl.performers.Performer;

public interface Result<T> {

	public Performer getPerformer();

	public T getResult();

}
