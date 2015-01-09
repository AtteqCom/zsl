<?php

namespace AtteqServiceLayer;

class TaskDecorator extends Task {
	
	protected $_task;
	
	function __construct(Task $task) {
		$this->_task = $task;
	}
	
	function get_name() {
		$this->_task->get_name();
	}
	
	function get_data() {
		$this->_task->get_data();
	}
}

class TaskResultDecorator extends TaskResult {
	
	protected $_task_result;
	
	function __construct(TaskResult $task_result) {
		$this->_task_result = $task_result;
	}
	
	function get_task() {
		$this->_task_result->get_task();
	}
	
	function get_result() {
		$this->_task_result->get_result();
	}
}

class JsonTaskDecorator extends TaskDecorator {

	function get_data() {
		$data = parent::get_data();
		return $this->_to_json($data);
	}

	private function _to_json($data) {
		return json_encode($data);
	}
}
