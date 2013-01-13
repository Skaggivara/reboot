$(document).ready(function(){
    
    var ROOT = "http://rebootmymovie.appspot.com/";
    var MOVIE_API_SEARCH_ENDPOINT = "http://api.themoviedb.org/3/search/movie";
    var MOVIE_API_DETAIL_ENDPOINT = "http://api.themoviedb.org/3/movie/";
    var MOVIE_API_KEY = "bc5116b9b7b4dceaadcc611420c14950";
    var MOVIE_POSTER_BASE_URL = "http://cf2.imgobject.com/t/p/";
    var MAX_NUM_RESULTS = 4;
    var SEARCH_INTERVAL_TIME = 400;
    var MESSAGE_INTERVAL_TIME = 5000;
    var FACEBOOK_MESSAGE = "I just voted for the movie '%' to be rebooted! Vote on the movie you would like to see rebooted at "+ ROOT;
    
    
    var current_movie = null;
    var search_interval = null;
    var message_interval = null;
    var latest_search = 0;
    
    function movie_detail(id, callback){
        var data = {
            "api_key": MOVIE_API_KEY
        };
        
        $.ajax({
            url: MOVIE_API_DETAIL_ENDPOINT + id,
            dataType: 'json',
            type: 'GET',
            data: data,
            success: function(data){
                if(callback){
                    callback(null, data);
                }
            },
            
            error: function(error){
                if(callback){
                    callback(new Error("Could not find movie detail."));
                }
            }
        });
    }
    
    function movie_exists(id, callback){
        
        $.ajax({
            url: ROOT + "movie/"+id,
            dataType: 'json',
            type: 'GET',
            success: function(data){
                if(callback){
                    callback(null, data);
                }
            },
            
            error: function(error){
                if(callback){
                    callback(new Error("Could not find movie."));
                }
            }
        });
    }
    
    function movie_create(details, callback){
        
        var data = {
            "facebook_uid" : details.facebook_uid,
            "facebook_token" : details.facebook_token,
            "facebook_name" : details.facebook_name,
            
            "title": details.title,
            "description": details.description,
            "year": details.year,
            "poster": details.poster,
            "imdb_id": details.imdb_id,
            "service_id": details.service_id,
            "csrf_token": details.csrf_token
        };
        
        $.ajax({
            url: ROOT + "movie/"+details.service_id,
            dataType: 'json',
            type: 'POST',
            data: data,
            success: function(data){
                if(callback){
                    callback(null, data);
                }
            },
            
            error: function(error){
                if(callback){
                    callback(new Error("Could not add movie."));
                }
            }
        });
        
    }
    
    function movie_vote(id, facebook_uid, facebook_token, facebook_name, callback){
        
        var data = {
            "service_id": id,
            "facebook_uid": facebook_uid,
            "facebook_token": facebook_token,
            "facebook_name": facebook_name,
            "csrf_token": $("#csrf_token").val()
        };
        
        $.ajax({
            url: ROOT + "vote/"+id,
            dataType: 'json',
            type: 'POST',
            data: data,
            success: function(data){
                if(callback){
                    callback(null, data);
                }
            },
            
            error: function(error){
                if(callback){
                    callback(new Error("You have already voted for that movie."));
                }
            }
        });
    }
    
    function handle_vote(details, callback){
        
        $("#loader").show();
        
        movie_exists(details.service_id, function(error, data){
            
            if(error){
                
                movie_create(details, function(error, data){
                    if(error){
                        if(callback) callback(error);
                        $("#loader").hide();
                        return;
                    }

                    movie_vote(details.service_id, details.facebook_uid, details.facebook_token, details.facebook_name, function(error, data){
                        if(error){
                            if(callback) callback(error);
                            $("#loader").hide();
                            return;
                        }
                        
                        $("#loader").hide();
                        
                        if (callback) callback(null, "Your vote has been registered!");
                        
                    });
                    
                });
                
            }else{
                
                movie_vote(details.service_id, details.facebook_uid, details.facebook_token, details.facebook_name, function(error, data){
                    if(error){
                        if(callback) callback(error);
                        $("#loader").hide();
                        return;
                    }
                    
                    $("#loader").hide();
                    
                    if (callback) callback(null, "Your vote has been registered!");
                });
            }
            
        });
        
    }
    
    function search(title, searchid, callback){
        
        var data = {
            "api_key": MOVIE_API_KEY,
            "query": clean(title)
        };
        
        $.ajax({
            url: MOVIE_API_SEARCH_ENDPOINT,
            dataType: 'json',
            type: 'GET',
            data: data,
            success: function(data){
                
                if(callback){
                    callback(null, data, searchid);
                }
            },
            
            error: function(error){
                
                if(callback){
                    callback(new Error("Could not find any movies."));
                }
            }
        });
    }
    
    function handle_search(){
        
        var query = $.trim(clean($("#search").val())).toLowerCase();
        
        if(query.length > 1){
            
            latest_search += 1;
            
            $("#searchform .loader").show();
        
            search(query, latest_search, function(error, data, searchid){
                
                if(error){
                    return;
                }
                
                if(data.results.length == 0){
                    var resultitem = "<li><div class='noresults'>No results found for: '<strong>"+query+"</strong>'</div></li>"; 
                    
                    $("#searchresult").html(resultitem);
                    
                    $("#searchform .loader").hide();
                    
                }else{
                    
                    if(latest_search === searchid){
                    
                        $("#searchresult").html("");
                        
                        $("#searchform .loader").hide();
                        
                        var numresults = 0;
                        
                        $("#searchclosebtn").show();
                        
                        var results = "";
                        
                        for(var i in data.results){
                            
                            if(!data.results[i].release_date){
                                data.results[i].release_date = "unknown";
                            }
                        
                            if(numresults < MAX_NUM_RESULTS){
                                var resultitem = "<li><a class='movie clearfix' href='#' data-id='"+data.results[i].id+"'><img src='"+MOVIE_POSTER_BASE_URL+"w92/"+data.results[i].poster_path+"' width='60' height='84' /><span class='title'>"+data.results[i].title+"</span><span class='desc'>"+data.results[i].release_date.split("-")[0]+"</span></a></li>"; 
                            
                                results += resultitem;
                            
                                numresults ++;
                            }
                        }
                    
                        $("#searchresult").html(results);
                    }
                }
                
                $("#searchresult").show();
                
            });
        }
    }
    
    function handle_error(error, silent){
        
        if(silent){
            console.log(error.message);
        }else{
            show_prompt(error.message);
        }
    }
    
    function show_prompt(msg){
        
        clearInterval(message_interval);
        
        $("#message p").html(msg);
        $("#message").show();
        
        message_interval = setTimeout(function(){
            $("#message").hide();
        }, MESSAGE_INTERVAL_TIME);
        
    }
    
    function login(callback){
        
        FB.login(function(response) {
            if (response.authResponse) {
                
                userdetails(function(error, details){
                    if(error){
                        if(callback) callback(error);
                    }else{
                        
                        details.id = response.authResponse.userID;
                        details.accessToken = response.authResponse.accessToken;
                        
                        if(callback) callback(null, details);
                    }
                });
            }else{
                if(callback) callback(new Error("Facebook login failed, please try again."));
            }
        }, {scope: 'email,user_photos,publish_stream'});
        
    }
    
    function authorize(callback){
        
        // here, first see that we are logged in with facebook
        // first we need to login to get user details...
        FB.getLoginStatus(function(response) {
            if(response.status === 'connected') {
                // the user is logged in and has authenticated your
                // app, and response.authResponse supplies
                // the user's ID, a valid access token, a signed
                // request, and the time the access token 
                // and signed request each expire
                var uid = response.authResponse.userID;
                var accessToken = response.authResponse.accessToken;
                        
                userdetails(function(error, user){
                    if(error){
                        if(callback){
                            callback(new Error("Facebook login failed, please try again."));
                        }
                    }else{
                        
                        if(callback){
                            callback(null, {
                                "facebook_token": accessToken,
                                "facebook_name": user.name,
                                "facebook_uid": uid
                            });
                        }
                    }
                });
                        
            }else{ // we are not logged in or approved
                
                login(function(error, user){
                    
                    if(error){
                        if(callback){
                            callback(error);
                        }
                    }else{
                        
                        if(callback){
                            callback(null, {
                                "facebook_token": user.accessToken,
                                "facebook_name": user.name,
                                "facebook_uid": user.id
                            });
                        }
                    } 
                });
            }
        });
    }
    
    function userdetails(callback){
        
        FB.api('/me', function(response) {
            if(response){
                if (callback) callback(null, {id: response.id, name: response.name});
            }else{
                if (callback) callback(new Error("Could not fetch user info."));
            }
        });
    }
    
    function post(message, image_url, callback){

        FB.api("/me/photos", "post", {
            url: image_url,
            message: message
        },
        function(response) {
            if (response && response.post_id) {
                if (callback) callback(null, response.post_id);
            } else {
                console.log(response);
                if (callback) callback(new Error("Image not uploaded"));
            }
        });
        
    }
    
    function clean(input){
        var no_tags = input.replace(/(<([^>]+)>)/ig,"");
        
        no_tags = $.trim(no_tags);
        no_tags = no_tags.replace(/(\r\n|\n|\r)/gm," ");
        return no_tags;
    }
    
    function update_search(){
        
        var thevalue = $.trim(clean($("#search").val())).toLowerCase();
        var current = $("#search").data("current");
        
        if(thevalue != current && thevalue.length > 1){
            
            $("#search").data("current", thevalue);
            
            handle_search();
            
        }
    }
    
    function update_votes(id){
        
        if($("#movie_"+id).length > 0){
            var current = parseInt($("#movie_"+id).data("votes"));
        
            $("#movie_"+id).data("votes", current+1);
        
            $("#movie_"+id+" .votes").html("("+(current+1)+" votes)");
        }
    }
    
    function update_movies(){
        
        var data = {
            "offset": 0,
            "limit": 11
        };
        
        $.ajax({
            url: ROOT + "movies",
            type: 'GET',
            data: data,
            success: function(data){
                $("#toplist ol").html(data);
            },
            
            error: function(error){
            }
        });
        
    }
    
    $("#searchresult .movie").live("click", function(e){
        e.preventDefault();
        
        movie_detail($(this).data("id"), function(error, data){
            
            if(!error){
                
                current_movie = data;

                $("#detail .info h3").html(data.title);
                
                var theyear = data.release_date;
                if(!theyear){
                    theyear = "unknown";
                }
                $("#detail .year").html(theyear.split("-")[0]);
                $("#detail .imdb a").attr("href", "http://www.imdb.com/title/" + data.imdb_id);
                $("#detail .votes").hide();
            
                $("#detail p").html(data.overview);
                
                if(data.poster_path){
                    $("#detail .poster img").attr("src", MOVIE_POSTER_BASE_URL + "w154" + data.poster_path);
                }else{
                    $("#detail .poster img").attr("src", "/static/img/noposter.jpg");
                }
            
                $("#detail").show();
                
                movie_exists(data.id, function(error, existing){
                    if(!error){
                        
                        var votestr = "vote";
                        
                        if(existing.votes != 1){
                            votestr = votestr+"s";
                        }
                        
                        $("#detail .votes").html("("+existing.votes+" "+votestr+"), ");
                        $("#detail .votes").show();
                    }
                });
                
            }
        });
        
        $("#searchresult").html("");
        $("#searchresult").hide();
        
        $("#search").data("current", "");
        $("#search").val("");
        $("#searchclosebtn").hide();
        
    });
    
    $("#search").on("focus", function(e){
        clearInterval(search_interval);
        search_interval = setInterval(function(){
            update_search();
        }, SEARCH_INTERVAL_TIME);
    });
    
    $("#search").on("blur", function(e){
        clearInterval(search_interval);
        
    });
    
    $("#searchform").on("submit", function(e){
        e.preventDefault();
        clearInterval(search_interval);
        handle_search();
    });
    
    $("#toplist .votebtn, #single .votebtn").live("click", function(e){
         e.preventDefault();
         
         if(!$(this).hasClass("loading")){
             
             $(this).addClass("loading");
             
             var theid = $(this).data("id");
             var thetitle = $(this).data("title");
             var theposter = $(this).data("poster");
         
             authorize(function(error, user){
                 if(error){
                     handle_error(error);
                     $("#movie_"+theid+" .votebtn").removeClass("loading");
                     return;
                 }
             
                 movie_vote(theid, user.facebook_uid, user.facebook_token, user.facebook_name, function(error){
                  
                      if(error){
                          
                          handle_error(new Error("You have already voted for that movie."));
                          
                          $("#movie_"+theid+" .votebtn").removeClass("loading");
                          
                          return;
                      }
                      
                      show_prompt("Your vote has been registered!");
                  
                      $("#movie_"+theid+" .votebtn").hide();
                      
                      post(FACEBOOK_MESSAGE.replace("%", thetitle), MOVIE_POSTER_BASE_URL + "w500" + theposter);
                      
                      update_votes(theid);
                  
                  });
             });
         }
    });
    
    $("#detail .votebtn").on("click", function(e){
        e.preventDefault();
        
        authorize(function(error, user){
            
            if(error){
                handle_error(error);
                return;
            }
            
            handle_vote({
                            
                "facebook_uid": user.facebook_uid,
                "facebook_token" : user.facebook_token,
                "facebook_name" : user.facebook_name,
                            
                "service_id": current_movie.id,
                "imdb_id": current_movie.imdb_id || "unknown",
                "title": current_movie.title,
                "year": current_movie.release_date,
                "description": current_movie.overview,
                "poster": current_movie.poster_path,
                "csrf_token": $("#csrf_token").val()
                            
            }, function(error, data){
                if(error){
                    handle_error(error);
                    return;
                }
                            
                show_prompt(data);
                
                update_votes(current_movie.id);
                
                post(FACEBOOK_MESSAGE.replace("%", current_movie.title), MOVIE_POSTER_BASE_URL + "w500" + current_movie.poster_path);
                
                update_movies();
                            
            });
            
        });
        
    });
    
    $("#detail .closebtn").on("click", function(e){
        e.preventDefault();
        $("#detail").hide();
        $("#loader").hide();
    });
    
    $("#searchclosebtn").on("click", function(e){
        e.preventDefault();
        $(this).hide();
        
        $("#search").data("current", "");
        $("#search").val("");
        $("#searchclosebtn").hide();
        
        $("#searchresult").hide();
        
        $("#search").focus();
    });
    
    $("#message .ok").on("click", function(e){
        e.preventDefault();
        $("#message").hide();
        clearInterval(message_interval);
    })
    
});
