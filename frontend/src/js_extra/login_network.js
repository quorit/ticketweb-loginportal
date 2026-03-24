

class NetworkError extends Error {
   constructor(message) {
      super(message);
      this.name="AuthSystemNetworkError"
   }
}

class HTTPResponseError extends NetworkError {
   //this error is for any http response error that is not failed session authentication
   constructor(status_code,message){
      super(message);
      this.status_code = status_code;
      this.name="AuthSystemHTTPResponseError"
   }
}





class ConnectionError extends NetworkError {
   //this is for when a fetch fails and we don't even get a response
   constructor(message){
      super(message);
      this.name="AuthSystemConnectionError"
   }
}





function test_ok(response) {
    return new Promise ((resolve,reject) => {
       if (response.ok){
          resolve (response);
       }else{
         var str = "Server returned " + response.status + " : " + response.statusText;
         if (response.status){

               reject(new HTTPResponseError(response.status,str));
                  
         }else{
            reject(new ConnectionError("No response status. Probably no connection to auth system"));
         }
       }
    });
}


function extended_fetch(opts,server_path){
   const url = window.location.origin + server_path + "login";

   return fetch(url,opts).then(response => response,err=> new ConnectionError(err.message));
}



function login(user_id, server_path){
   
   const body = JSON.stringify({
      user_id: user_id
   });
   return extended_fetch(
      {   
         method: "POST",
         mode: "cors",
         body: body
      },
      server_path)
      .then(response => test_ok(response))
      .then(response => response.text())
}





export {login,
        ConnectionError,
        HTTPResponseError,
        NetworkError     
      }
