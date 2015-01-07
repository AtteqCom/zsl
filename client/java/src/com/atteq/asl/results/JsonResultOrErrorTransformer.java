package com.atteq.asl.results;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import org.apache.commons.httpclient.HttpStatus;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.JavaType;

import com.atteq.asl.performers.Performer;

public class JsonResultOrErrorTransformer<ResultType, ErrorType extends Error> implements
		ResultTransformer<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> {

	protected ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory;
	protected ObjectMapper mapper = new ObjectMapper();

	public JsonResultOrErrorTransformer(
			ResultFactory<ResultOrError<ResultType, ErrorType>, GenericResult<ResultOrError<ResultType, ErrorType>>> factory) {
		this.factory = factory;
	}

	public JavaType getType(Class<ResultType> resultClass, Class<ErrorType> errorClass) {
		return mapper.getTypeFactory().constructParametricType(ResultOrError.class, resultClass, errorClass);
	}

	@Override
	public GenericResult<ResultOrError<ResultType, ErrorType>> transform(Performer performer, String result,
			int status, JavaType type) throws TransformationException {
		final DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
		mapper.setDateFormat(df);
		try {
			ResultOrError<ResultType, ErrorType> r;

			try {
				if (status == HttpStatus.SC_OK) {
					ResultType rr = mapper.readValue(result, type.containedType(0));
					r = new ResultOrError<ResultType, ErrorType>(rr);
				} else {
					ErrorType error = mapper.readValue(result, type.containedType(1));
					r = new ResultOrError<ResultType, ErrorType>(error);
				}
			} catch (JsonMappingException _e) {
				ErrorType error = mapper.readValue(result, type.containedType(1));
				r = new ResultOrError<ResultType, ErrorType>(error);
			}
			return factory.create(performer, r);
		} catch (Exception e) {
			throw new TransformationException(e);
		}
	}

}
