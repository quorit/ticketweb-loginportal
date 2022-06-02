class WebProjectError extends Error {
    constructor(message) {
       super(message);
       this.name="WebProjectError"
    }
}




class FormValidationError extends WebProjectError {
    //this is for when a fetch fails and we don't even get a response
    constructor(){
       super("Form validation error");
       this.name="FormValidationError";
    }
}

class HTTPResponseError extends WebProjectError {
    //this error is for any http response error that is not failed session authentication
    constructor(status_code,message){
       super(message);
       this.status_code = status_code;
       this.name="HTTPResponseError"
    }
 }


function get_error_params(e){
    var return_val={};
    if (e instanceof WebProjectError){
        return_val.error_type = e.name;
        if (e instanceof HTTPResponseError){
            return_val.status_code=e.status_code.toString();
        }
    }else{
        return_val.error_type = "Uncategorized";
    }
    return return_val;
}

export {WebProjectError,FormValidationError,HTTPResponseError,get_error_params}
