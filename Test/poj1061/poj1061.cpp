#include<iostream>
#include<cstdio>
using namespace std;

long long ex_gcd(long long a, long long b, long long &x, long long &y)
{
    //ax+by=gcd(a,b);
    if(b==0){
        x=a; 			// error!!! should be x=1;
		y=0;
        return a;
    }
    long long r=ex_gcd(b,a%b,y,x);
    y-=x*(a/b);
    return r;
}

int main()
{
    long long x,y,m,n,l;
    while(scanf("%lld %lld %lld %lld %lld",&x,&y,&m,&n,&l)!=EOF){
		long long d, t, p;
        long long a, r;
        a=((m-n)%l+l)%l;
        r=((y-x)%l+l)%l;
        d=ex_gcd(a, l, t, p);
        //printf("%lld %lld %lld %lld\n",a,t,l,p);
        if(r%d!=0) printf("Impossible\n");
        else{
            t=(t%l+l)%l;
            t=r/d*t%l;
            printf("%d\n",t);	// error!!! should be print("%lld\n, t");
        }
	}
    
    return 0; 	
}
