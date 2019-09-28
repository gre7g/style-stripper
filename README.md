# style-stripper
## Credit
Project and code—Gre7g Luterman <gre7g.luterman@gmail.com>
## Contributing
Pull requests and translations are welcome.

I haven't created many templates as of yet. If you want one that isn't yet supported and don't want to make it yourself, consider supporting the project with a donation. E-mail me the details of how you want the template to look and send a $10 (or more) donation to my PayPal (same address as my e-mail) and I'll add it to the project. Template details are listed at the end of this README.
## Notes
Code is able to extract most details from the template files but the docx library doesn't include methods for a couple things. To work around that, I've encoded the last few things I care about in the file name and the template's comment string.
### File Name
* Dimensions such as 5x8 to mean 5" x 8"
* "bleed" if the template allows for full-bleed images
### Comment String Format
Comment strings is a CSV of numbers such as 1,395,0. Fields mean the following:
* Header/footer arrangement variant:
  * 1—even-header=centered author's name, odd-header=centered book title, footers=outer margin aligned page numbers
* Average number of pages this template will generate with a 100,000 word manuscript
* Section headings:
  * 0—Heading 1=chapter
  * 1—Heading 1=part, Heading 2=chapter
## Template Details
* Final book dimensions
* Supports full-bleed images or not
* Body text font, size, and line spacing
* Header/footer arrangement, font, size, heights
* Margins
