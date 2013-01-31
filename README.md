Django hash field
=================

Custom field to Django, storing the hashed value of some other field.

Problem
-------

MySQL doesn't allow to create indexes on text fields, whose length is greater than 255 ([or something like that]
(http://lmgtfy.com/?q=mysql+255+index)). This can be a practical problem if you want to store a list of unique
urls in your database (accepted length of url is up to 2083 characters).

Solution
--------

The good solution to this problem is to create two columns in your database:

  1. column of length 2083, storing the raw url address
  2. column of length 40, storing hashed value of url

Then create an index on the second column. Class HashField implements a custom field in Django, which
autoamtically stores the hashed value of the original field (such as url field) everytime the model is saved.

Example
-------

Using HashField, you can store the list of unique urls in Django as follows:

    class VisitedSite(models.Model):
      url = models.URLField(max_length=2083)
      url_hash = HashField(original='url', unique=True)

      def __unicode__(self):
        return self.url
    ...

    site = VisitedSite(url='http://github.com')
    site.save() # url_hash is automatically computed and saved to database
