# CTF
It's a CTF!

web app with XSS vulnerabilities


## Achievements

#### signup
go to the site, choose a name (I don't think this should be the case)

#### find login
inspect `index.html`

#### xss alert
chuck a `<script>alert()</script>` in a comment/post

#### redirect page
`<script>window.location="http://evilsite.io"</script>` in a comment/post

#### password: mel
sql inject to get the users table, then reverse the md5 hash (it's a common one, just google the hash)

#### stolen token
fire up wireshark and snag someone's token over wifi (the expiration has to be beyond now? this may be difficult)

#### find hidden path
`/hidden`

#### break server
probably the same as sql-error below

#### sql-error
in a verify credentials (login) request, use a username with a `;` which should screw up the db query for validate user, causing an exception to get raised (no guarantees, pretty sure about this)
