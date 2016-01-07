package com.atteq.asl.utils;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import com.fasterxml.jackson.databind.ObjectMapper;

public class JsonHelper {

	public static ObjectMapper createMapper() {
		ObjectMapper mapper = new ObjectMapper();
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		return mapper;
	}

}
