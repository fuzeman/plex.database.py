0.8.0 (2016-09-06)
------------------
**Added**
 - Methods
    - :code:`MovieLibrary`
        - :code:`count(sections, [account])`
    - :code:`ShowLibrary`
        - :code:`count(sections, [account])`
    - :code:`EpisodeLibrary`
        - :code:`count(sections)`
        - :code:`count_items(sections)`

**Changed**
 - All exceptions raised by "tzlocal" are now caught (unknown timezone, etc..)
 - Warning is now displayed if the "LIBRARY_DB" variable hasn't been defined
 - :code:`MovieLibrary.mapped()` now returns the :code:`MediaPart.duration` and :code:`MediaPart.file` fields
 - Enabled strict guid parsing

0.7.0 (2015-09-12)
------------------
 - Initial release
