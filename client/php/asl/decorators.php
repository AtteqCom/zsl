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


class SecuredTaskDecorator extends TaskDecorator {
	
	private $_allowed_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz';
	private $_random_token_length = 16;
	
	function get_data() {
		$random_token = $this->_get_random_token();
		
		return array(
			'data' => $this->_task->get_data(),
			'security' => array(
				'random_token' => $random_token,
				'hashed_token' => $this->_compute_hashed_token($random_token),
			),
		);
	}
	
	function set_asl(Service $asl) {
		$this->_asl = $asl;
	}
	
	private function _get_random_token() {
		$token = '';
		
		for ($i = 0; $i < $this->_random_token_length; $i++) {
			$token .= $this->_get_random_allowed_character();
		}
		
		return $token;
	}
	
	private function _get_random_allowed_character() {
		return $this->_allowed_characters[\rand(0, strlen($this->_allowed_characters) - 1)];
	}
	
	private function _compute_hashed_token($random_token) {
		$hash = \sha1($random_token . $this->_asl->get_secure_token());
		return \strtoupper($hash);
	}
}
