<?php

namespace AtteqServiceLayer;

abstract class TaskResult {
	
	abstract function get_task();
	abstract function get_result();

}

class RawTaskResult extends TaskResult {

	protected $_task;
	protected $_result;

	function __construct(Task $task, $result) {
		$this->_task = $task;
		$this->_result = $result;
	}

	function get_task() {
		return $this->_task;
	}

	function get_result() {
		return $this->_result;
	}
}
