



class FormValidationError extends Error {
    //this is for when a fetch fails and we don't even get a response
    constructor(){
       super("Form validation error");
       this.name="FormValidationError";
    }
}



export {FormValidationError}
