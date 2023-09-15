简短易懂的代码：

```cpp

#include<iostream>
#include<cstring>
using namespace std;
char a1[50001],b1[50001];
int a[50001],b[50001],i,x,len,j,c[50001];
int main ()
{
    cin >>a1 >>b1;\/\/读入两个数
    a[0]=strlen(a1);b[0]=strlen(b1);\/\/计算长度
    for (i=1;i<=a[0];++i)a[i]=a1[a[0]-i]-'0';\/\/将字符串转换成数字
    for (i=1;i<=b[0];++i)b[i]=b1[b[0]-i]-'0';
    for (i=1;i<=a[0];++i)for (j=1;j<=b[0];++j)c[i+j-1]+=a[i]*b[j];\/\/按乘法
    len=a[0]+b[0];                                       \/\/原理进行高精乘
    for (i=1;i<len;++i)if (c[i]>9){c[i+1]+=c[i]\/10;c[i]%=10;}\/\/进位
    while (c[len]==0&&len>1)len--;\/\/判断位数
    for (i=len;i>=1;--i)cout <<c[i];\/\/输出
    return 0;
}

```
```cpp
var a,b:ansistring;
    le:boolean;
    c,d,e:array[0..20000]of longint;
    i,j:longint;
begin
  readln(a);
  readln(b);
  for i:=length(a) downto 1 do
   val(a[i],c[length(a)-i+1]);
  for i:=length(b) downto 1 do
   val(b[i],d[length(b)-i+1]);
  for i:=1 to length(a) do
   for j:=1 to length(b) do
     inc(e[i+j-1],c[i]*d[j]);
  for i:=1 to (length(a)+length(b)) do
   if e[i]>9 then
   begin
     e[i+1]:=e[i+1]+e[i] div 10;
     e[i]:=e[i] mod 10;
   end;
  le:=false;
  for i:=(length(a)+length(b)) downto 1 do
   if le=false then begin if e[i]<>0 then begin le:=true; write(e[i]); end; end
               else write(e[i]);
  if le=false then writeln(0);
end.
```