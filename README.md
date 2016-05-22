# QUESTIONS

## WORKSPACE ENVIRONMENT

1. With what version of python do you work?
> Python 2.7
  
2. Django version?
> 1.9

3. Do you have a ssh access to your server. If so I will need a ssh public key for deployment.
> Yes

4. Server config (for deployment). It  number of processor`s cores and memory.
>

## PROJECT

1. Is REST interface required?
> Required.
2. That project. (my task). Will it be absolutely independent project from other part? 
Or it will using the same database?
> It`s part of one big project. Currently it is part 2. 
Later we will have to merge all parts into one project. 
Maybe it will necessarily to completely rewrite the first part.

3. Can we use postgres db (it will depends on django features and sql table structure)?
>

## PROJECT`S APPLICATIONS

### ACCOUNTS (login page task and user account)

1. Only login page, without registration?
> Later. But it is necessary to make if we will remake the first part.

2. What does means that string "Location: State:City:District:Street:Building:NO." ?
Does it describes a fields in the db? Or is it a format of one db field? 
If it is a list of db fields: should state and city be represented by own tables
 and referenced by foreign keys in the user table?
> Db table for each reference + representing string.

3. Pretty strange to have a "brand name" at user model/table. 
> Brand is for the STORE!

4. Does one store should be belong to the ONE user?
> Yes.

5. Does vendors (users) will be the only kind of users?
> No.

6. Can user (vendor) see and use records (size, color, brand, etc) made by other vendors?
>

7. Who creates the store?
>

8. Does store creates after new user(vendor)? Or does store creates before the new user?
>

### COMMODITY

1. Commodity model / table structure. Does catalog, size, color and etc 
should be references to another tables (foreign keys)? Or it is just CHAR values?
> Tables.

2. I need a logic (pseudo-code) generating and a sample of RFID code.
> Waiting...

3. What does it mean &mdash; "commodity tag". What it should looks like?
> User customs tags (structure depends of db). Each commodity can has a multiple tags.
The relation structure between commodity table and tag depends of the db choice. 
POSTGRES IS BETTER. But it is up to you. 

4. For what purpose are these tags? I need to imagine how they will be used?

5. Only authenticated user can access to commodity views?
> Yes.

6. Does each user must have his own data with colors, sizes, brands, etc?
>
