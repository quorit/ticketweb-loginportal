const base_year = "1901";
const base_strm = "1011";

function term_lookup(strm){
   const last_digit = strm.slice(-1);
   const base_year_int = parseInt(base_year);
   const base_strm_int = parseInt(base_strm);
   const season_lookup = {
      '1': 'Winter',
      '5': 'Summer',
      '9': 'Fall'
   }
   const season = season_lookup[last_digit];
   const strm_int = parseInt(strm);
   const year_delta = Math.floor((strm_int-base_strm_int)/10);
   const year = base_year_int + year_delta;
   return year.toString() + " " + season;
}


function get_current_term(){
    var today = new Date();
    var m = String(today.getMonth())
    var yyyy = today.getFullYear();
    const base_year_int = parseInt(base_year);
    const base_strm_int = parseInt(base_strm);
    var seasonOffset;
    if (m >=0 && m<= 3) {
        seasonOffset = 0;
    }else if(m >= 4 && m <=7){
        seasonOffset = 4;
    }else{
        seasonOffset = 8;
    }
    const year_delta = yyyy - base_year_int;
    const strm_int = (year_delta * 10) + base_strm_int + seasonOffset;
    return strm_int.toString();
}


function get_strm_bounds(current_term){
    const strm_int = parseInt(current_term);
    const begin = (strm_int - 20).toString();
    const end = (strm_int + 10).toString();
    return {
        begin: begin,
        end: end
    }
}


function strm_get_prev(strm){
    const last_digit = strm.slice(-1);
    const strm_int = parseInt(strm);
    const subtraction_lookup = {
      '1': 2,
      '5': 4,
      '9': 4
    }
    const subtraction = subtraction_lookup[last_digit];
    const prev_strm_int = strm_int - subtraction;
    return prev_strm_int.toString();
}



export {term_lookup, get_strm_bounds, strm_get_prev, get_current_term};