## Cloudflare Assessment

### Setup Steps / Summary

*   First, I began writing a basic flask app to return all of the headers with a GET request to the /headers endpoint. From there, I used a commonn Dockerfile based on the Google Cloud docs to build the image and run the container. Initially, I deployed to Cloud Run, as it is an easy way to deploy containers, but I realized for this assessment I would need more control to place the Cloudflare signed certificate on the server as well as setting up a Cloudflare tunnel that has local network access to the application. It is definitely possible to do this with Cloud Run and a multistage Dockerfile, but I decided to use a Compute Engine instance instead.
*   From there, I deployed a micro N1 GCE instance running a Debian 10 image. I installed Docker on the instance and cloned my application repo, which can be found here: [Cloudflare Assessment](https://github.com/ckahle33/cf-test). I used the Cloudflare GCP setup documentation to set up apach2 which is serving the root index.html file. Nginx would normally be my webserver of choice, but Apache2 ease-of-use won out here. The provided link on how to add a Cloudflare signed cert was very useful here.
*   I then used the provided Cloudflare Tunnels Docker command to run the tunnel on the instance. I used the --no-autoupdate flag to prevent the tunnel from updating and breaking the application. I also used the -d flag to daemonize the process. The Cloudflare tunnel product is excellent, and very useful for exposing private services publically. I really like how easy it is to run the tunnel in a Docker container with the provided command from the UI. The only gotcha I ran into was neededing to add the `--network host` flag, which I had to use to allow the tunnel to access the application on `localhost:5000`.
*   I then cloned my application repo using `git clone "https://github.com/ckahle33/cf-test"`, built and ran my Flask application using `docker build -t flask-app .` and `docker run -p 5000:5000 flask-app`
*   I decided to structure the application as a kitchen sink with multiple routes that solve the problems in the assessment. I used the `flask` and `requests` libraries to build the application. Requests made it straightforward to loop through and display the headers in the /headers route.
*   I wrote a scoped API call to grab all of the DNS records associated with my Cloudflare zone. The docs were solid here, but was slighlty misled because I needed to add the `Authorization Bearer:` bearer header instead of the `X-Api-Key` header that was suggested in the docs. It is possible I misread the docs, but I was able to get it working with the bearer header.

### Did you learn anything new during this assignment?

Yes, I learned about the Cloudflare Tunnel product, which is excellent! It was nice to get a refresher on installing certs onto a server, which has been a while

### How did you fill the gaps (if any) in your knowledge during the process?

I mainly consulted the Cloudflare docs and GCP docs. The provded documentation was strong

### What was your experience with Cloudflare Zero Trust, Cloudflare Tunnels and Cloudflare Workers?

I really like Cloudflare Tunnels, and Workers. I am still getting used to Zero Trust, but can already see how it would be very helpful to lock down routes of an application super quickly. I switched to the Wrangler CLI for Workers, and it is very easy to use. I like how it is a wrapper around the API, and I can use it to quickly deploy and update my worker. It felt like writing a familiar node app where I could add dependencies and use npm to manage them.

### What issues did you run into (if any) and how did you overcome them?

The only issues I ran into were pivoting to a Compute Engine instance instead of Cloud Run, and getting the Cloudflare tunnel to work with the application by using the `--network host` flag. Cloud Run just announced support for sidecar and proxy containers, which would have made this easier, but is definitely a bleeding edge feature, thus GCE made more sense for now.

### How would you describe each product in simple language?

Cloudflare Tunnel: A way to expose private services publically

Cloudflare Workers: A way to run serverless code on the edge

Cloudflare Zero Trust: A way to lock down routes of an application

### What use cases can you see each product being useful for?

Cloudflare Tunnel: This honestly can and will hopefully usher a move away from using VPNs for securing private resources. VPNs definitely will have their place, but this is a great alternative for exposing private services publically, very quickly.

Cloudflare Workers: I really like this product in that you can build complete applications eg. html/react that some other FaaS (function as a service) providers do not allow, or make it complicated to do. These applications could pair very nicely with larger infrastructure and handle crons or data movement/pipelines.

Cloudflare Zero Trust:

### How do you imagine that a target customer will find this experience?

I believe the products are very strong and easy to use. The documentation is excellent as well. I really liked seeing the diverse array of Worker examples that used the Wrangler CLI. The only slightly confusing aspect I encountered is that Zero Trust products use a separate dashboard than dash.cloudflare.com