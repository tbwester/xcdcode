///////////////////////////////////////////
// Thomas Wester
// University of Chicago
// Autumn 2015
// 
///////////////////////////////////////////

#include"TFile.h"
#include"TMultiGraph.h"
#include"TLine.h"
#include"TGraph.h"
#include"TGraphErrors.h"
#include"TCanvas.h"
#include"TPad.h"
#include"TPaveText.h"
#include"TAxis.h"
#include"TMath.h"
#include"TStyle.h"
#include"TFrame.h"
#include"TLegend.h"
#include"TH1F.h"
#include"TF1.h"

#include<string>
#include<vector>
#include<sstream>
#include<fstream>
#include<iomanip>

using namespace std;

string toString(double d);
void stability() {

  TCanvas *c1 = new TCanvas("c1","c1",1000,800);
  TCanvas *c2 = new TCanvas("c2", "c2", 1000,800);
 
  c1->cd();

  ifstream fin;
  fin.open("runlist.txt");

  vector<float> x;
  vector<float> y;
  vector<float> xerr;
  vector<float> yerr;
  
  vector<float> y2;
  vector<float> y2err;

  vector<float> pey0, pey1, pey2;
  vector<float> pey0err, pey1err, pey2err;
    
  //Read in each line of the runlist.txt file.
  int runCounter = 0;
  string RunName;
  while (fin >> RunName) {
      
    x.push_back(runCounter); //("Run" + RunName);    
    xerr.push_back(0.);

    //Create a string for the run's root file.
    string filepath = "/data/xcd/processed/v1_0_0/";
    string filename = filepath + "Run" + RunName + ".root";
    
    cout << filename.c_str() << endl;

    //Extract the plot from the run's root file.
    TFile *f1 = TFile::Open(filename.c_str());
    TH1D *h1 = (TH1D *)f1->Get("channel_0_laser_int_hist");

    //Fit 0 pe peak
    TF1* gaus0 = new TF1("gaus0","[0]*TMath::Exp(-0.5*((x-[1])/[2])^2)",-10,10);
    gaus0->SetParameter(0,1);
    gaus0->SetParameter(1, 0);
    gaus0->SetParameter(2, 10);

    //Fit 1 pe peak
    TF1* gaus1 = new TF1("gaus1","[0]*TMath::Exp(-0.5*((x-[1])/[2])^2)",125,190);
    gaus1->SetParameter(0,1);
    gaus1->SetParameter(1, 150);
    gaus1->SetParameter(2, 80);

    //Fit 2 pe peak
    TF1* gaus2 = new TF1("gaus2","[0]*TMath::Exp(-0.5*((x-[1])/[2])^2)",250,325);
    gaus2->SetParameter(0,1);
    gaus2->SetParameter(1, 290);
    gaus2->SetParameter(2, 100);

    h1->Fit("gaus0","R","",-10,10);
    h1->Fit("gaus1","R+","",125,190);
    h1->Fit("gaus2","R+","",250,325);
    
    string outfile = "hist2/" + RunName + ".root";
    TFile f(outfile.c_str(),"RECREATE");
    h1->Write(RunName.c_str());
  
    TF1 *fit0 = (TF1 *)h1->GetFunction("gaus0");
    Double_t yval0 = fit0->GetParameter(0); //fit0->Eval(fit0->GetParameter(1)); 
    Double_t yvalerr0 = fit0->GetParError(0);
                        //TMath::Abs(fit0->Eval(fit0->GetParameter(1) + 
                        //                      fit0->GetParError(1)) - yval0);
  
    TF1 *fit1 = (TF1 *)h1->GetFunction("gaus1");
    Double_t yval1 = fit1->GetParameter(0); //fit1->Eval(fit1->GetParameter(1)); 
    Double_t yvalerr1 = fit1->GetParError(0);
                        //TMath::Abs(fit1->Eval(fit1->GetParameter(1) + 
                        //                      fit1->GetParError(1)) - yval1);

    TF1 *fit2 = (TF1 *)h1->GetFunction("gaus2");
    Double_t yval2 = fit2->GetParameter(0); //fit1->Eval(fit1->GetParameter(1)); 
    Double_t yvalerr2 = fit2->GetParError(0);
                        //TMath::Abs(fit1->Eval(fit1->GetParameter(1) + 
                        //                      fit1->GetParError(1)) - yval1);

    cout << yval0 << "\t\t" << yvalerr0 << endl;

    //Store the individual counts before dividing
    pey0.push_back(yval0);
    pey1.push_back(yval1);
    pey2.push_back(yval2);

    pey0err.push_back(yvalerr0);
    pey1err.push_back(yvalerr1);
    pey2err.push_back(yvalerr2);

    y.push_back(yval0 / yval1);
    yerr.push_back(TMath::Sqrt((yvalerr0/yval0)*(yvalerr0/yval0) + 
                   (yvalerr1/yval1)*(yvalerr1/yval1)) * (yval0/yval1));  

    y2.push_back(yval0 / yval2);
    y2err.push_back(TMath::Sqrt((yvalerr0/yval0)*(yvalerr0/yval0) + 
                   (yvalerr2/yval2)*(yvalerr2/yval2)) * (yval0/yval2));  

    runCounter++;
  }

  fin.close();

  TMultiGraph *mg = new TMultiGraph();

  TGraphErrors *gr = new TGraphErrors(x.size(), &(x[0]), &(y[0]), 
                                                &(xerr[0]), &(yerr[0]));

  TGraphErrors *gr2 = new TGraphErrors(x.size(), &(x[0]), &(y2[0]), 
                                                 &(xerr[0]), &(y2err[0]));


  TPaveText *pt = new TPaveText(.05,.7,.25,.8,"brNDC");
  string meanStr = "0pe/1pe Mean: " + toString(gr->GetMean(2));
  string rmsStr = "0pe/1pe RMS: " + toString(gr->GetRMS(2));
  string meanStr2 = "0pe/2pe Mean: " + toString(gr2->GetMean(2));
  string rmsStr2 = "0pe/2pe RMS: " + toString(gr2->GetRMS(2));
  
  pt->AddText(meanStr.c_str());
  pt->AddText(rmsStr.c_str());
  pt->AddText(meanStr2.c_str());
  pt->AddText(rmsStr2.c_str());

  gr->SetMarkerStyle(7);
  gr2->SetMarkerStyle(7);
  
  gr->SetMarkerColor(2);
  gr2->SetMarkerColor(4);

  int xmin = *min_element(x.begin(),x.end());
  int xmax = *max_element(x.begin(),x.end());
/*
  TF1* flat = new TF1("flat","[0]", xmin, xmax);
  flat->SetParameter(0,gr->GetMean(2));
 
  gr->Fit("flat","R","", xmin, xmax);
  TF1 *flatfit = (TF1 *)gr->GetFunction("flat");

  double rcs = flatfit->GetChisquare() / flatfit->GetNDF();
*/
  fin.open("runlist.txt");
  int PointCounter = 0; //Stores the number of points to plot
  while (fin >> RunName) {
      int bin_index = gr->GetXaxis()->FindBin(x[PointCounter]);
      gr->GetXaxis()->SetBinLabel(bin_index, RunName.c_str());

      int bin_index2 = gr2->GetXaxis()->FindBin(x[PointCounter]);
      gr2->GetXaxis()->SetBinLabel(bin_index2, RunName.c_str());
      PointCounter++;
  }
  fin.close();
  
  //gStyle->SetOptStat(1011);

  gr->GetXaxis()->SetLabelSize(0.02);
  gr->GetXaxis()->LabelsOption("h");
  gr2->GetXaxis()->LabelsOption("h");
  gr->GetXaxis()->SetTitle("Run #");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->SetTitle("0 PE Counts / 1 PE Counts");
  gr->GetYaxis()->CenterTitle();

  gr->GetXaxis()->SetRangeUser(xmin - 1, xmax + 1);
  gr2->GetXaxis()->SetRangeUser(xmin -1, xmax + 1);
  gr->SetTitle("Ratio of 0 Photoelectrons to Single Photoelectrons");
  gr->SetMarkerColor(2);
  gr2->SetTitle("Ratio of 0 Photoelectrons to Two Photoelectrons");
  gr->SetMarkerColor(2);
  gr->SetMarkerStyle(7);
  //gr->Draw("AP");
  gr2->Draw("AP");
/*  
  mg->Add(gr);
  mg->Add(gr2);

  mg->Draw("AP");
  mg->GetYaxis()->SetTitle("Ratio of Counts");
  mg->GetXaxis()->SetTitle("Run Number");
*/
  pt->Draw();

  TLegend* leg = new TLegend(0.45,0.8,0.65,0.88);
  leg->SetHeader("Legend");
  leg->AddEntry(gr,"0pe/1pe","ep");
  leg->AddEntry(gr2,"0pe/2pe","ep");
  leg->Draw();

  c2->cd();
  
  TMultiGraph *mg2 = new TMultiGraph();

  TGraphErrors *gry0 = new TGraphErrors(x.size(), &(x[0]), &(pey0[0]), 
                                                &(xerr[0]), &(pey0err[0]));

  TGraphErrors *gry1 = new TGraphErrors(x.size(), &(x[0]), &(pey1[0]), 
                                                 &(xerr[0]), &(pey1err[0]));

  TGraphErrors *gry2 = new TGraphErrors(x.size(), &(x[0]), &(pey2[0]), 
                                                 &(xerr[0]), &(pey2err[0]));

  gry0->SetMarkerStyle(7);
  gry1->SetMarkerStyle(7);
  gry2->SetMarkerStyle(7);
   
  gry0->SetMarkerColor(2);
  gry1->SetMarkerColor(4);
  gry2->SetMarkerColor(6);

  mg2->Add(gry0);
  mg2->Add(gry1);
  mg2->Add(gry2);

  mg2->Draw("AP");
  mg2->GetYaxis()->SetTitle("Counts");
  mg2->GetXaxis()->SetTitle("Run Number");

  TLegend* leg2 = new TLegend(0.45,0.8,0.65,0.88);
  leg2->SetHeader("Legend");
  leg2->AddEntry(gry0,"0pe","ep");
  leg2->AddEntry(gry1,"1pe","ep");
  leg2->AddEntry(gry2,"2pe","ep");
  leg2->Draw();

  c2->SaveAs("c2.pdf");

  cout << gr->GetMean(2) << ", " << gr->GetRMS(2) << endl;

  for(std::vector<int>::size_type i = 0; i != x.size(); i++) {
    std::cout << x[i] << "\t\t" << y[i] << "\t\t" << yerr[i] << endl;
  }
}

string toString(double d) {
  stringstream ss;
  ss << d;
  return ss.str();
}
