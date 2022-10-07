#pragma once

#include "TOPP.h"
#include "KinematicLimits.h"
#include "TorqueLimits.h"
#include "PolygonConstraints.h"

#include <boost/format.hpp>

//SO3 constraints
// #include "SO3Constraints.h"


using namespace TOPP;

class TOPPInstance {
public:
    TOPPInstance(std::string problemtype, std::string constraintsstring, std::string trajectorystring){

        TOPP::Trajectory* ptrajectory = new TOPP::Trajectory(trajectorystring);

        if (problemtype.compare("KinematicLimits")==0) {
            pconstraints.reset(new KinematicLimits(constraintsstring));
            pconstraints->trajectory = *ptrajectory;
        }
        else if (problemtype.compare("TorqueLimits")==0) {
            pconstraints.reset(new TorqueLimits(constraintsstring));
            pconstraints->trajectory = *ptrajectory;
        }
        else if (problemtype.compare("PolygonConstraints")==0) {
            pconstraints.reset(new PolygonConstraints(constraintsstring));
            pconstraints->trajectory = *ptrajectory;
        }
        else if (problemtype.compare("QuadraticConstraints")==0) {
            pconstraints.reset(new QuadraticConstraints(constraintsstring));
            pconstraints->trajectory = *ptrajectory;
            pconstraints->CheckInput();
        }
        else {
            throw TOPP_EXCEPTION_FORMAT("cannot create %s problem type", problemtype, 0);
        }

        // Set default public tuning parameters
        integrationtimestep = 0;
        passswitchpointnsteps = 5;
        extrareps = 0;

        // Set default private tuning parameters
        pconstraints->bisectionprecision = 0.01;
        pconstraints->loweringcoef = 0.95;
    }

    boost::shared_ptr<Constraints> pconstraints;
    TOPP::Trajectory restrajectory;

    std::string outconstraintstring;
    std::string restrajectorystring;
    std::string resextrastring;
    std::string resprofilesliststring;
    std::string switchpointsliststring;
    int ntangenttreated;
    int nsingulartreated;
    TOPP::dReal resduration;
    TOPP::dReal sdendmin, sdendmax;
    TOPP::dReal sdbegmin, sdbegmax;

    // Tuning parameters
    TOPP::dReal integrationtimestep;
    int passswitchpointnsteps, extrareps;

    TOPP::dReal GetAlpha(TOPP::dReal s, TOPP::dReal sd) {
        std::pair<TOPP::dReal, TOPP::dReal> sdd_lim = pconstraints->SddLimits(s, sd);
        return sdd_lim.first;
    }


    TOPP::dReal GetBeta(TOPP::dReal s, TOPP::dReal sd) {
        std::pair<TOPP::dReal, TOPP::dReal> sdd_lim = pconstraints->SddLimits(s, sd);
        return sdd_lim.second;
    }


    int RunComputeProfiles(TOPP::dReal sdbeg, TOPP::dReal sdend){
        // Set tuning parameters

        pconstraints->integrationtimestep = integrationtimestep;
        pconstraints->passswitchpointnsteps = passswitchpointnsteps;
        pconstraints->extrareps = extrareps;
        pconstraints->stepthresh = 0.01;

        int res = ComputeProfiles(*pconstraints,sdbeg,sdend);

        resduration = pconstraints->resduration;
        return res;
    }


    int ReparameterizeTrajectory(TOPP::dReal reparamtimestep=0)
    {
        // Set tuning parameters
        pconstraints->reparamtimestep = reparamtimestep;

        int ret = pconstraints->trajectory.Reparameterize(*pconstraints, restrajectory);
        return ret;
    }


    int RunAVP(TOPP::dReal sdbeg1, TOPP::dReal sdbeg2){
        // Set tuning parameters
        pconstraints->integrationtimestep = integrationtimestep;
        pconstraints->passswitchpointnsteps = passswitchpointnsteps;
        pconstraints->extrareps = extrareps;

        sdbegmin = sdbeg1;
        sdbegmax = sdbeg2;
        int ret = AVP(*pconstraints, sdbegmin, sdbegmax,
                      sdendmin, sdendmax);
        if(ret == 0) {
            sdendmin = -1;
            sdendmax = -1;
        }
        return ret;
    }

    int RunAVPBackward(TOPP::dReal sdend1, TOPP::dReal sdend2){
        // Set tuning parameters
        pconstraints->integrationtimestep = integrationtimestep;
        pconstraints->passswitchpointnsteps = passswitchpointnsteps;
        pconstraints->extrareps = extrareps;

        sdendmin = sdend1;
        sdendmax = sdend2;
        int ret = AVPBackward(*pconstraints, sdbegmin, sdbegmax,
                              sdendmin, sdendmax);
        if(ret == 0) {
            sdbegmin = -1;
            sdbegmax = -1;
        }
        return ret;
    }

    void WriteResultTrajectory(){
        // std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        // printf("WriteResultTrajectory: %d %f %d blah\n",
        //        restrajectory.dimension, restrajectory.duration,
        //        restrajectory.degree);
        std::stringstream ss;
        ss << std::setprecision(17);
        restrajectory.Write(ss);
        restrajectorystring = ss.str();
    }

    void WriteProfilesList(){
        std::list<Profile>::iterator itprofile = pconstraints->resprofileslist.begin();
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        std::stringstream ss;
        ss << std::setprecision(17);

        TOPP::dReal dt = 1e-4;
        pconstraints->WriteMVCBobrow(ss,dt);
        ss << "\n";
        pconstraints->WriteMVCDirect(ss,dt);
        ss << "\n";
        while(itprofile!=pconstraints->resprofileslist.end()) {
            itprofile->Write(ss,dt);
            ss << "\n";
            itprofile++;
        }
        resprofilesliststring = ss.str();
    }

    std::string SerializeInputTrajectory() {
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        std::stringstream ss;
        ss << std::setprecision(17);

        pconstraints->trajectory.Write(ss);
        return ss.str();
    }

    void WriteSwitchPointsList(){
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        std::stringstream ss;
        ss << std::setprecision(17);
        std::list<SwitchPoint>::iterator itsw = pconstraints->switchpointslist.begin();
        while(itsw != pconstraints->switchpointslist.end()) {
            ss << itsw->s << " " << itsw->sd << " " << itsw->switchpointtype << "\n";
            itsw++;
        }
        switchpointsliststring = ss.str();
        ntangenttreated = pconstraints->ntangenttreated;
        nsingulartreated = pconstraints->nsingulartreated;
    }

    // Write Constraints (currently works only for QuadraticConstraints)
    void WriteConstraints(){
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        std::stringstream ss;
        ss << std::setprecision(17);

        pconstraints->WriteConstraints(ss);
        outconstraintstring = ss.str();
    }

    // Extra string, such as the coordinates of the ZMP (depending on the application)
    void WriteExtra(){
        //std::stringstream ss; ss << std::setprecision(std::numeric_limits<OpenRAVE::dReal>::digits10+1);
        std::stringstream ss;
        ss << std::setprecision(17);
        pconstraints->WriteExtra(ss);
        resextrastring = ss.str();
    }

};