class WebProjectError extends Error {
    constructor(message) {
       super(message);
       this.name="WebProjectError"
    }
}


export {WebProjectError,FormValidationError}


class FormValidationError extends WebProjectError {
    //this is for when a fetch fails and we don't even get a response
    constructor(){
       super("Form validation error");
       this.name="FormValidationError";
    }
}