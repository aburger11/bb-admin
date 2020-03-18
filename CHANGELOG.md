# 0.1.1
* Bugfix: branch restriction config: An extra restriction was preventing master and develop from being able to be merged in PRs
* Bugfix: branch restriction config: hotfixes were deletable but bugfixes were not - swapped them.

# 0.1.0
* Added more configs and updated README
* Added: Docker steps
* Check if repo exists already, check status codes, custom exception, cleanup
* Added: A couple unit tests
* Moved create method calls to caller
* Verify user can auth & is admin before attempting to do anything.
* Tweak: No newline on print(...) lines & added "done." prints
* Tweak: No more double declaration for api endpoints
* Added: BitBucketAdmin superclass & moved a couple methods there
* Added: Can create inside and outside of projects. Works in private test space as well as social-solutions space.
* Added: Convert users to uuids, branch restrictions, model, default reviewers, pipelines, purge and create environments
* Initial commits
