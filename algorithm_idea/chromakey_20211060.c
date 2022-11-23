/* C code
The below code is a C implementation of this algorithm. 
It is very simple, and uses windows bmp files for input and output. 
The strange format of the bmp file somewhat obscures the logic, 
but all of the stuff is there. In AOI aware Java the looping would be much better, 
and the images are already im memory, this version was designed to use almost no memory 
(only 1 pixel at a time is in memory) and have no external dependancies.
It also was my first C program in like 7 years. */


/* a fast implementation of the chromakey program
(c) 2008 Edward Cannon
feel free to use or modify at will */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int max(int a, int b)
{
   if (a>b) {return (a);}
   return (b);
}

/*the follwing three functions convert RGB into YCbCr in the same manner as in JPEG images*/

int rgb2y (int r, int g, int b)
{
   /*a utility function to convert colors in RGB into YCbCr*/
   int y;
   y = (int) round(0.299*r + 0.587*g + 0.114*b);
   return (y);
}

int rgb2cb (int r, int g, int b)
{
   /*a utility function to convert colors in RGB into YCbCr*/
   int cb;
   cb = (int) round(128 + -0.168736*r - 0.331264*g + 0.5*b);
   return (cb);
}

int rgb2cr (int r, int g, int b)
{
   /*a utility function to convert colors in RGB into YCbCr*/
   int cr;
   cr = (int) round(128 + 0.5*r - 0.418688*g - 0.081312*b);
   return (cr);
}

double colorclose(int Cb_p,int Cr_p,int Cb_key,int Cr_key,int tola,int tolb)
{
   /*decides if a color is close to the specified hue*/
   double temp = sqrt((Cb_key-Cb_p)*(Cb_key-Cb_p)+(Cr_key-Cr_p)*(Cr_key-Cr_p));
   if (temp < tola) {return (0.0);}
   if (temp < tolb) {return ((temp-tola)/(tolb-tola));}
   return (1.0);
}

int get32(FILE * f)
{
   /*reads a 32 bit int from file*/
   int a, b, c, d;
   a = getc(f);
   b = getc(f);
   c = getc(f);
   d = getc(f);
   /*printf("get32 %i %i %i %i
", a, b, c, d);*/
   return (a + 256*b + 65536*c + 16777216*d);
}
struct bmp
{
   int valid;
   int filesize;
   int datapos;
   int width;
   int height;
   FILE * file;
};

struct bmp readBMPheader(const char * filename)
{
   /*reads the BMP header and decides if everything is ok, returns a struct bmp*/
   FILE * file;
   char b, m;
   int in;
   struct bmp thisfile;
   file = fopen(filename, "rb");
   if (file == NULL)
   {
      thisfile.valid = 0;
      return (thisfile);
   }
   /*check magic number*/
   b = (char) getc(file);
   m = (char) getc(file);
   /*printf("test");*/
   if (b != 'B' || m != 'M')
   {
      thisfile.valid=0;
      return (thisfile);
   }
   /*printf("%c%c", b, m);*/
   thisfile.valid = 1;
   thisfile.file = file;
   thisfile.filesize = get32(file);
   /*skip past reserved section*/
   getc(file);
   getc(file);
   getc(file);
   getc(file);
   thisfile.datapos = get32(file);
   /*get width and height from fixed positions*/
   fseek(file, 18, SEEK_SET);
   thisfile.width = get32(file);
   thisfile.height = get32(file);
   return (thisfile);
}

struct bmp writeBMP(const char * filename, struct bmp example)
{
   /*returns a struct bmp with the header written and its file open for writting data
   copies header information from example, makes file right size filled with black*/
   int i;
   struct bmp thisfile;
   thisfile.file = fopen(filename, "wb");
   if (thisfile.file == NULL)
   {
      thisfile.valid = 0;
      return (thisfile);
   }
   fseek(example.file, 0, SEEK_SET);
   for(i=0;i; ){
      fputc(getc(example.file), thisfile.file);
   }
   for(i=0;i;)    {
      fputc(0, thisfile.file);
   }
   return (thisfile);
}

int main (int argc, char *argv[])
{
   /*must be 8 command line arguments
   filenames fg, bg, out, r, g, b, tola, tolb*/
   if (argc != 9)
   {
      printf("must be 8 command line arguments\n");
      printf(" fg bg out r g b tola tolb");
      return(1);
   }
   int b, g, r, y, cb, cr, r_bg, g_bg, b_bg;
   int b_key, g_key, r_key, cb_key, cr_key, tola, tolb;
   int pos, mx;
   double mask;
   struct bmp fg, bg, out;
   /*set up for chromakey */
   fg = readBMPheader(argv[1]);
   bg = readBMPheader(argv[2]);
   out = writeBMP(argv[3], fg);
   r_key = atoi(argv[4]);
   g_key = atoi(argv[5]);
   b_key = atoi(argv[6]);
   cb_key = rgb2cb(r_key, g_key, b_key);
   cr_key = rgb2cr(r_key, g_key, b_key);
   tola = atoi(argv[7]);
   tolb = atoi(argv[8]);
   /*loop through file and preform chromakey*/
   pos = fg.datapos;
   mx = 3*fg.width;
   switch (mx%4)
   {
   case 1:
      mx = mx+3;
      break;
   case 2:
      mx = mx+2;
      break;
   case 3:
      mx = mx+1;
      break;
   }
   int i, j;
   for (i=0; i;)    {
      fseek(fg.file, pos, SEEK_SET);
      fseek(out.file, pos, SEEK_SET);
      fseek(bg.file, pos, SEEK_SET);
      for (j=pos; j;)       {
         b = getc(fg.file);
         g = getc(fg.file);
         r = getc(fg.file);
         b_bg = getc(bg.file);
         g_bg = getc(bg.file);
         r_bg = getc(bg.file);
         cb = rgb2cb(r,g,b);
         cr = rgb2cr(r,g,b);
         mask = colorclose(cb, cr, cb_key, cr_key, tola, tolb);
         mask = 1 - mask;
         r = max(r - mask*r_key, 0) + mask*r_bg;
         g = max(g - mask*g_key, 0) + mask*g_bg;
         b = max(b - mask*b_key, 0) + mask*b_bg;
         fputc(b, out.file);
         fputc(g, out.file);
         fputc(r, out.file);
      }
   pos = mx+pos;
   /*printf("\n");*/
   }
   /*close files and clean up*/
   fclose(fg.file);
   fclose(bg.file);
   fclose(out.file);
   return (0);
}
