


const authsystem_network = require ("authsystem_network");

const rt_network = require ("rt_network");



class FormValidationError extends Error {
    //this is for when a fetch fails and we don't even get a response
    constructor(){
       super("Form validation error");
       this.name="FormValidationError";
    }
}




function get_error_params(e){
    var return_val={};
    if (e instanceof FormValidationError || e instanceof rt_network.NetworkError || e instanceof authsystem_network.NetworkError){
        return_val.error_type = e.name;
        if (e instanceof rt_network.HTTPResponseError || e instanceof authsystem_network.HTTPResponseError){
            const status_code = e.status_code.toString() || "0";
            return_val.status_code=status_code;
        }
    }else{
        return_val.error_type = "Uncategorized";
    }
    return return_val;
}

export {FormValidationError,get_error_params}
