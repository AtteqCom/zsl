<?php

namespace AtteqServiceLayer;

abstract class Task {
	
	abstract function get_name();
	abstract function get_data();
}

class RawTask extends Task {

	protected $_name;
	protected $_data;

	function __construct($name, $data) {
		$this->_name = $name;
		$this->_data = $data;
	}

	function get_name() {
		return $this->_name;
	}

	function get_data() {
		return $this->_data;
	}
}
