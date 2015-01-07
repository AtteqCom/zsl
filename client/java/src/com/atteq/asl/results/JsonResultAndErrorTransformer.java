package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import org.apache.log4j.Logger;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;

public class JsonResultAndErrorTransformer<ResultType, ErrorType extends Error> implements ResultTransformer<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> {

	protected ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory;

	Logger logger = Logger.getLogger(getClass());

	public JsonResultAndErrorTransformer(ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory) {
		this.factory = factory;
	}

	@Override
	public GenericResult<ResultOrError<ResultType, ErrorType>> transform(Performer performer, String result, int status, JavaType type) throws TransformationException {
		ObjectMapper mapper = new ObjectMapper();
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		try {
			logger.debug(String.format("Response:\n%s", result));
			ResultOrError<ResultType, ErrorType> r;

			try {
				ResultType rr = mapper.readValue(result, type.containedType(0));
				r = new ResultOrError<ResultType, ErrorType>(rr);
			} catch (JsonMappingException _e){
				ErrorType error = mapper.readValue(result, type.containedType(1));
				r = new ResultOrError<ResultType, ErrorType>(error);
			}
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
