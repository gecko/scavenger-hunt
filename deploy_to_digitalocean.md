# Deploy to `digitalocean.com`

- Sign up to digitalocean.com
- Create a droplet in a project
  - Select a droplet from the marketplace
  - Ubuntu with docker
  - Select a payment plan (I used all low)
  - Enable a static, or public, or whatever it is named IP adress.
  - Connect that IP with your domain name (e.g. at regfish)

- Open a terminal in your droplet
  - `git clone https://github.com/gecko/scavenger-hunt.git`
  - `cd scavenger-hunt`
  - `sudo ufw enable`
  - `sudo ufw allow 80 && sudo ufw allow 443`
  - `sudo ufw reload`
  - `sudo apt install nginx`
  - `sudo nano /etc/nginx/sites-available/scavenger-hunt`
  - Put in the following content:
    ```shell
    server {
      listen 80;
      server_name scavenger.gecko.org;
      location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
      }
    }
    ```
  - `sudo ln -s /etc/nginx/sites-available/scavenger-hunt /etc/nginx/sites-enabled/`
  - Run `sudo nginx -t` just to verify the config
  - `sudo systemctl reload nginx`
