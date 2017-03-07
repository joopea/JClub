backend s3 {
  .host = "joopea-dev.s3.eu-central-1.amazonaws.com";
  .port = "80";
}

sub vcl_recv {

    unset req.http.cookie;
    unset req.http.cache-control;
    unset req.http.pragma;
    unset req.http.expires;
    unset req.http.etag;
    unset req.http.X-Forwarded-For;

    if (req.request != "GET") {
        return(pipe);
    }

    set req.http.host = "joopea-dev.s3.eu-central-1.amazonaws.com";
#    set req.url = "filer_public_thumbnails" + req.url;

    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(jpg|png|gif|gz|tgz|bz2|tbz|mp3|ogg)$") {
            remove req.http.Accept-Encoding;
        } elsif (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } elsif (req.http.Accept-Encoding ~ "deflate") {
            set req.http.Accept-Encoding = "deflate";
        } else {
            remove req.http.Accept-Encoding;
        }
    }

    return(lookup);

}

sub vcl_hash {
    hash_data(req.url);
    return(hash);
}

sub vcl_fetch {
    unset beresp.http.X-Amz-Id-2;
    unset beresp.http.X-Amz-Meta-Group;
    unset beresp.http.X-Amz-Meta-Owner;
    unset beresp.http.X-Amz-Meta-Permissions;
    unset beresp.http.X-Amz-Request-Id;
    unset beresp.http.cookie;
    unset beresp.http.cache-control;
    unset beresp.http.pragma;
    unset beresp.http.expires;
    unset beresp.http.etag;
    unset beresp.http.X-Forwarded-For;
    unset beresp.http.Server;

    set beresp.grace = 6h;
    set beresp.ttl = 1w;

    return(deliver);

}

sub vcl_deliver {
    unset resp.http.Via;
    unset resp.http.X-Varnish;
}
