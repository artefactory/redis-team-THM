## About Redis

Redis is an open source in memory NoSQL database it was created in 2009 by Salvatore Sanfilippo.

Redis primary use is when you have a database like MongoDB, SQL server, MySQL, and parts of your website or your application need to get data more quicker than your database can.

You would host part of the data in memory as a cache in Redis.
Redis can handle data structures such as Strings, Lists, Sets, Sorted Sets and Hashes and also more advanced one.

Frequent use cases: store your sessions in Redis, keep a list of most recent visitors, compare which one of your friends are my friends, implement the pub/sub pattern.

If you want to do something that's interactive or
something where they're getting the most
recent let's say post to website like
what Twitter does that needs to be done
more in a structured way and Redis is perfect for that.


if you want enterprise cluster Redis

labs company I work for offers that you

can get a free download you can also use

Redis cloud also by our company this is

Redis as a service upon Amazon on Azure

on Google on IBM's clouds so we run it

in all of those clouds and there's lots

of other companies out there so you can

go to read a screen open Redis again

Redis cloud and read us to go these are

all different rhetta's as a service

providers even Amazon ElastiCache is

based on Redis so and as yours cache is

also based on reddit so Retta so again

let's go into some details here so you

know what is Redis so very specifically

some people you've probably heard the

term you know key value store so Redis

isn't really a traditional key value

where the value is a string it's would

call a key data structures server or

store and what that means is it has more

than just string values that get stored

in cache you can store data that's more

like a database and there's different

types of data types data values so you

can have strings lists sets sorted sets

and hashes the hash is kind of like a

hash table so that's very similar to a

table you can also have bitmaps in

memory and there's something called a

hyper log log which I'll talk about

briefly it's kind of a new thing

it runs in memory as I said before which

means it's extremely fast both for reads

and writes and it does have disk

persistence so you can have a log and

you can capture the data so that you're

storing it on disk and therefore if

something were to happen it goes down

you can survive the crash it'll load

back up for you and your because it all

only runs in memory your limitation

primarily is the memory available on

that particular server you can cluster

Redis you can do it with the open-source

version however if you need help or if

you feel like you just rather have

somebody provide you the technology that

does all that that's what our company

does

but let's move on to how Redis is used

so it's like I said it's extremely easy

to use it's very well-documented up on

rehto scott io so you know go take a

look there's lots of good useful

information there most people use it as

a cache or as a second database so if

you've got a database on your server

that's saving your data on disk but you

are having problems scaling that you can

use Redis not only to cache but also to

keep the data from the database in

memory so you can query it and some

folks actually do use it as a

first-class database and in other words

you don't have another database this is

their only database usually you might do

that if the data that you're keeping in

your database isn't very useful after a

short period of time like for example on

high-frequency trading or something like

that where all the data is really

happening in real time and you know

maybe you stream it off and store it

somewhere as a log but you don't really

need to keep that data if we're to go

down it wouldn't be useful to bring it

back up because time is already passed

so who is using Redis there's a lot of

different companies I mentioned before

you can go take a look at this URL and

see tons of companies using it and by

the way oh I forgot to mention it's also

great for other things like pub/sub a

lot of folks user for pub/sub so what

that means is you have a lot of web

browsers open and they're all viewing a

shared set of data then you can have

them subscribe to Redis which will then

let them know when a change occurs and

they can all update their browsers

simultaneously I've actually written an

application and using node.js for that

and there's a configuration file that

you set up it's really simple so it's

actually quite simple to set up

individually it's also single threaded

this is kind of interesting so what that

means is it's only doing one action at a

time so accuse them all up and it does

them all on in a row this actually helps

with performance because you don't have

to worry about a record being locked

it's just doing one action after another

there is no locking because of that so

and it's lightning fast that it actually is quite

hard to give it so many requests that it

can't handle the load although you can

that can't happen so it's it's

incredibly fast and the single foot it

actually helps with that which this

means though is you tend to shard if you

run out of memory you need more space

you tend to shard your database so you

might have transactions A through F on

this database on the server you know G

through I don't know m on this server

and n through Z on another server so

that's that might be typically how you

were to scale and okay so I mentioned

earlier or maybe I didn't but anyway

it's it's often compared to Memcached

Redis actually supports Memcached for

the most part so a lot of folks actually

have used them cache D might switch over

to Redis because they got they get the

Memcached functionality plus

the Redis functionality and it's just as

fast as Memcached for most in most

cases and again you get this rich set of

data not just key value pairs you get to

store data in a structure so you can do

querying in memory and it does support

persistence so you know if your server

goes down you don't have to your server

might have to come back up or you can

recover from another server but you can

recover all the memory at once you don't

have to wait for it to rebuild which can

be very slow and painful and it does

replication through a master slave

concept so you can have a set of your

data in memory on one server it can keep

a copy in another server that means if

when if your primary server were to go

down it can immediately switch over to

use the copy and then therefore you

don't have any downtime and in a very

common scenario you would actually have

a master slave scenario where the master

is doing all the interacting with your

applications and the slave is actually

doing this saving to disk so they both

have their their role and you can

perform better that way so what are some

more use cases oops somehow we lost air

we go okay that's funny so what are some

use cases um

one example is you might show the last

items listed on a website on your

webpage you know eBay postings are

listing something like that obviously at

some point you need to remove them so

you'd have delete deleting or filtering

based on certain criteria you do that -

that would be hard to do in a cache

where there's no idea of individual

records that are in a set a leaderboard

actually makes a lot of sense with Redis

so you might have a bunch of users all

competing and then based on criteria you

can very quickly and easily filter that

data and show you know the top players

of all time top players this month top

players today top players right now all

that could be in memory and sorted

quickly and displayed in real time also

user voting you can use a sorted set

which I'll talk about a little bit where

you can let people vote and then you've

got your names of people or ideas or

products or whatever you're voting on

and then your votes that can all be kept

in memory in real time and you can

expire items so for example this is

great for things where you know that you

don't want that information to display

after a certain period of time you can

set an expiration date on the record and

then it will automatically you don't

have to go back and remove it it'll

automatically remove itself from the

list and therefore automatically stop

displaying on the webpage at that time

so a lot of very useful functions now

I've got more for you counting stuff

that's probably pretty easy to do unique

items so they've got some functionality

where you can say add this to the list

but only if it doesn't exist on the list

already and you don't have to worry

about writing that functionality right

Caching is very popular with Redis.

With high speed data where you're trying to keep your
website responding to really unusual
usage patterns that your database wasn't
really designed for rather than trying
to model something very cleverly so that
you can take your model and mirror it on
the website and keep updating your model
to match the performance required.


The best probable scenario is just simply
take the data keep it the way it's
stored the way you need it to be stored
in your own system but then remodel it
using something like Redis and just put
it in a way that it's going to perform
better for your website and you can you
know you can take in each individual use
case and customize it for that
particular scenario so that it performs
quickly.


be as fast so instead you can call the

function have all the work done on the

server and then you're done rather than

getting the data pulling it

back doing the work that you need to be

done and then resubmitting it to the

database that's not likely to be as fast

so there's a bunch of data types I don't

have a I don't have a any much more than

this so I'm going to go through some

data types for you and then we'll be

done so let's just take a quick look you

got your string okay it's more or less

what you think it might be

Storing data using JSON.



for a cache you can put up images and


kind of thing lots of different use

cases where you just don't need to go

put all this in your database lists so

these are just internally maintained as

link lists they're extremely fast

especially towards the beginning in the

end of the list so you know very long

lists and you can use this again for

like queues or just stacks of data top

and recent news that

thing and this is what a lot of folks

use for social networks so this is what

you know Twitter uses you know pretty

much all those social websites are using

this functionality and use for for

logging users actions this are pop

l.push is what I talked about earlier

where you can kind of take an item out

of a queue and stick it in another queue

all in one function we also have sets

sets is just simply a unique list so you

throw some data in there if it's already

in there I just ignores it it doesn't

add it again or you can use sets to

compare one set with another set so

you're friends with my friends we can

very quickly figure out which friends we

have in common you can find out you know

hey here's a here's does this number

already exist that kind of thing lots of

very simple but very highly effective

and fast functionality again it's great

for storing social data here are some

functions oops that kind of got whacked

out so you've got some tracking IP

tracking IP unique IPS to your website

so if for example if you're trying to

defend against the DDoS or something

like that you can use this functionality

to say you know what I've gotten too

many requests from this website in the

short period of time you can set the

automatically expire so that you can set

it off it you know 10 seconds or

something like that and if if a person

keeps coming back more than two or three

times per 10 seconds you might decide

that's something unusual you know used

to tagging information creating random

numbers so you can respond for ads or

lottery information tips of the day that

kind of stuff that's all great for in

memory let's try that page is a little

off you can a sorted set a sorted sets

kind of interesting because you can add

a value to the number or

a value to the data so this is how you

would keep track of like if people are

voting and you have a value next to the

list of data and therefore you can have

a sorted vote on a sorted list

essentially our sorted set and basically

it's behaves just like sets except for

you have that that value next to it and

it's still extremely fast and the the

the queries are very fast because it all

the sorting happens immediately upon

insert so the queries are always going

against static data it's very fast and

again for using examples like a

leaderboard top lists of anything you

can index other data so if you have hash

tables or other lists you can index them

using a sorted set that references off

to another structured type you can click

for example querying for a range of

users all given a date or age or some

other characteristic and finally of the

five main types you got the hash and

hash is kind of like a table very

similar to a table and so you've got the

value like a unique user ID and then you

got all the additional values that are

stored along with it it's you can kind

of nest one hash within another but then

that's about as far as you can go and

you can refer to each one of the values

individually and you can even sort them

so it can behave more or less like a

regular table this is where you would

store data if you're storing data for

for example in a business object for

example you know like maybe a person and

their characteristics

Book [Redis in Action](https://www.goodreads.com/book/show/16033444-redis-in-action)