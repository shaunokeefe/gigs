# Adding Data
## CSV Imports
CSV imports are currently performed using the Django Admin Inerface.
### Log In
Go to the URL for the Django Admin Interface (http://\<the url of the current deployment\>/admin/)

Log in as prompted (you'll need to be an admin to do this - contact the site admin if you're not!)

### Start adding a cvs import

On the site administration page, there will be a list of applications (auth, cvsimport, gig_registry etc.).
You want to add a cvsimport so in the cvsimport app, select the 'add' button next to the cvsimport model entry.

This should take you to the http://\<your url\>/admin/csvimport/csvimport/add/ page

From here you will add a description of the CVS info you're looking to import, and the django app will then 
attempt to import it for you. 

### Select the model you're importing

Each import you do will deal primarily with one model type  (e.g. locations, venues, gigs). A single import 
can deal with multiple models in a single spreadsheet (e.g. a spreadsheet that lists both information about a 
venue and information about its location), but best results, you should try to 
[normalise](http://en.wikipedia.org/wiki/Database_normalization) your data as best as possible.

Choose gig_registry.\<model\>, replacing \<model\> with the name of the model that your spreadsheet deals with.
The prefix 'gig_registry' simply specifies the django application the model belongs to. All the imports you'll be
doing are for models in gig_registry, so don't worry about this too much.

### Prepare your spreadsheet
While you can leave your spreadsheet largely in its current format when importing, there are two requirements:

1. It will need to be in CSV format. This means that if you're working in XLS, you'll need to save the specific sheet
that contains your data to a separate CSV file (File -> save as -> choose 'CSV' for the format and 'ok' when prompted
that this will onl save the active sheet)

2. Mark up the columns, telling the cvsimport application which columns in your spreadsheet map to which field in the
model you're importing. The application doesn't enforce a strict layout for your spreadsheet (e.g. first field is
'street name', second is 'postcode' etc.). Instead, it allows you to add a cell to the top of each column to tell it
what data each column contains. So, if you're importing location data, like the following:
<table>
  <tr>
    <td>3121</td>
    <td>57 Swan St</td>
    <td>Richmond</td>
  </tr>
</table>
Then you need to mark it up like this:
<table>
  <tr>
    <td>post_code</td>
    <td>street_address</td>
    <td>suburb</td>
  </tr>
  <tr>
    <td>3121</td>
    <td>57 Swan St</td>
    <td>Richmond</td>
  </tr>
</table>
This simply tells the importer to create a location model instance with the street address '57 Swan St', the suburb
'Richmond', and the post code '3121'

The naming of the fields is pretty specific (e.g. 'postcode' wont work - it has to be 'post_code' as this is the name
of the field in the data model). Here's a list of all the field names you can use in each of the core models:

* Locations
 * street_address
 * country
 * state
 * suburb
 * post_code
 * lat\*\*\*
 * lon\*\*\*
* Venue
 * uid
 * name
 * location\*
 * established
 * stages
 * venue_type
 * status
 * status_notes
 * comment
* Gig
 * start
 * finish
 * venue\*
 * name
 * cost
 * comment
* Band
 * name
 * genre\*\*
 * members\*\*
 * founded


\* This is a 'foreign key' entry. See 'Related Fields' below.

\*\* This is a 'many to many' entry. See Many to Many Fields below.

\*\*\* Latitude and Longitude can be manually entered, but TUGG will also try
to work them out for you automatically anyway. It will also try to guess any missing fields
from location data using the Google Maps API.

### Choose your file
After you have marked up your spreadsheet and exported the relevant sheet to a csv file, choose the 'choose file' button next to 'Upload File' and browse to and select your CSV file. 

### Running the import
Select 'Save and continue editing' on the add csvimport page and the importer will attempt to import your data into TUGG. Any erros will be listed in the 'Error log' field.

### Related Fields
It is possible to import multiple different models (remember, models are *types* of data, not individual entries) from  a single spreadhseet. For example, if you have a list of venues with their addresses in a spreadsheet, you can mark your spreadsheet up so that the csvimporter will split each row into a location model isntance and a venue model instance and then link them in the database.

For example, your data might look like this:

<table>
  <tr>
    <td>The Corner Hotel</td>
    <td>3121</td>
    <td>57 Swan St</td>
    <td>Richmond</td>
  </tr>
</table>
  <tr>

Then you'll need to mark it up like this:

<table>
  <tr>
    <td>name</td>
    <td>location.post_code</td>
    <td>location.street_address</td>
    <td>location.suburb</td>
  </tr>
  <tr>
    <td>The Corner Hotel</td>
    <td>3121</td>
    <td>57 Swan St</td>
    <td>Richmond</td>
  </tr>
</table>

What was that all about? Well, firstly, you need to tell the importer which models you want which fields to be mapped
to. This wasn't necesary in the earlier example as you were only importing one type of model. Now you're importing two - 
a location and a venue. So, here we prefix all the location model's fields with 'location.' to tell the importer they 
go into the location model. Why aren't the venue fields prefixed with 'venue'? Because you only have to specify the model
type for 'child' models. You select the model type for the parent from the 'Model name' drop down box on the 'Add csv
import' page as mentioned earlier. That is, for the example, you'll choose 'gig_registry.venue'.

...What's a child/parent? Easy; describe the relationship by saying 'A has a B'. 'B' is the child. In this case, it's 'A 
venuehas a location', and the location is the child. Likewise, if you had a sheet with a gig, a venue, and a location 
on each row, the location would be the child of the venue, and the venue the child of the gig, with the gig being the parent.
You'd prefix all location fields with 'venue.location.', all venue fields with 'venue.', and choose 'gig_registry.gig'
from the 'Model name' drop down box on the 'Add csv import' page.

When you import the sheet, the importer will do something extra. As well as creating instancesof the primary 
'parent' models for each row, it will also create related child data. First, it will search for existing data
that matches the fields specified for the child. In our example, it will look for the location '57 Swan St Richmond VIC 
312' in the database. If it finds it, it will skip creating it and instead, simply link the venue to that location. 
It will then create the parent as usual.

### Many to Many Fields
A number of fields in the models are Many to Many fields. For example 'bands' in the 'gigs' model. This simply 
means that each gig can have many bands, and each band can have played at many gigs. 

If you want to specify a gig with a number of related bands in a single spreadsheet, you need to use slightly special
mark up. Rather than prefixing fields with 'bands.' as we've done in earlier examples, you'll need to mark each field
'bands.1.', 'bands.2.' and so forth, in order to specify which of the multiple bands you're adding each field belongs
to. For example, you have two bands, The Wild Cherries and The cherokees. Above the cell containing the name 'The Wild
Cherries', you'd enter 'bands.1.name', and abovve the cell containing the name 'The Cherokees' you'd enter 'bands.2.name'.
