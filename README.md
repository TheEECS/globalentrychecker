# globalentrychecker
A tool built with Python (2.7) and Selenium to check latest global entry times and schedule an earlier time

## Installation
### Required
1. You need [Python](https://www.python.org/).  I used Python 2.7, but imagine it should work fine for 3 if that's what you have
2. This tool requires you to have [Selenium](http://selenium-python.readthedocs.io/installation.html) set up

### Optional
- If you'd like to run off Chrome you also need to get [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- If you want to email yourself with Gmail you'll likely need to turn on ["Allowing Less Secure Apps"](https://support.google.com/accounts/answer/6010255?hl=en)

## Usage
- The script can be run manually or set it to run on a cron job.
-- Edit with crontab -e and enter the below.
-- Example: Run every 30 minutes between 7 a.m. to 9 p.m.
```
*/30 7-21 * * * python /path/to/script
```

## Limitations/TODOs
- Doesn't go any more granular than days (could look at parsing into hours)
- Consider whitelist hours along

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History
- 2/6/17 Create and share!

## License

MIT or see LICENSE