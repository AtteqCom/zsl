<?php

abstract class Service {

	/**
	 * Connects to Service Layer and call task on it.
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
	 * @param array (of strings) $decorators - array of TaskDecorator / TaskResultDecorator
	 * 		subclass names
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
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class($decorator, 'TaskDecorator')) {
				$task = new $decorator($task);
			}
		}

		return $task;
	}
	
	private function _apply_task_result_decorators(TaskResult $task_result,
		$decorators) {
		
		foreach ($decorators as $decorator) {
			if ($this->_is_subclass_or_same_class($decorator, 'TaskResultDecorator')) {
				$task_result = new $decorator($task_result);
			}
		}

		return $task_result;
	}
	
	private function _is_subclass_or_same_class($tested_class_name, $class_name) {
		return $tested_class_name == $class_name || is_subclass_of(
			$tested_class_name, $class_name);
	}
}
