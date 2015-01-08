<?php

abstract class Service {

	/**
	 * Connects to Service Layer and assigns task to it.
	 * 
	 * @param string $task_name - name of the task
	 * @param $task_data - input data for the task
	 * @return unprocessed result of call to Service Layer
	 */
	abstract protected function _inner_call($task_name, $task_data) {}

	/**
	 * Calls given task. Task data will be processed by TaskDecorator's given in
	 * $decorators array.
	 * 
	 * @param Task $task - task to be called
	 * @param array $decorators - array of TaskDecorator's / TaskResultDecorator's
	 * @return result processed by TaskResultDecorator's given in $decorators array 
	 */
	function call(Task $task, $decorators = array()) {
		$call_task_result = $this->_call_task($task, $decorators);
		return $this->_process_call_task_result($call_task_result, $decorators); 
	}
	
	private function _call_task(Task $task, $decorators) {
		$task = $this->_apply_task_decorators($task, $decorators);
		
		$task_data = $task->get_data();
		$task_name = $task->get_name();
		
		return $this->_inner_call($task_name, $task_data);
	}
	
	private function _process_call_task_result($call_task_result, $decorators) {
		$task_result = new RawTaskResult($task, $call_task_result);
		return $this->_apply_task_result_decorators($task_result, $decorators);
	}

	private function _apply_task_decorators(Task $task, $decorators) {
		return $task;
	}
	
	private function _apply_task_result_decorators(TaskResult $task_result,
		$decorators) {
		
		return $task_result;
	}
}
