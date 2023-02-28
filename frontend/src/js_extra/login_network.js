

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
         console.log("About to resolve response");
          resolve (response);
       }else{
         console.log("bye son");
         console.log(response);
         console.log(response.status);
         var str = "Server returned " + response.status + " : " + response.statusText;
         if (response.status){

               reject(new HTTPResponseError(response.status,str));
                  
         }else{
            reject(new ConnectionError("No response status. Probably no connection to auth system"));
         }
       }
    });
}


function extended_fetch(opts,server_path,app_key){
   const url = window.location.origin + server_path + "login/" + app_key;

   return fetch(url,opts).then(response => response,err=> new ConnectionError(err.message));
}



function login(user_id, password,server_path,app_key){
   
   const body = JSON.stringify({
      user_id: user_id,
      password: password
   });
   return extended_fetch(
      {   
         method: "POST",
         mode: "cors",
         body: body
      },
      server_path,
      app_key)
      .then(response => test_ok(response))
      .then(response => response.json())
}





export {login,
        ConnectionError,
        HTTPResponseError,
        NetworkError     
      }
