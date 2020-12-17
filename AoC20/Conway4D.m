classdef Conway4D
    properties
        Matrix
        MatrixSize
        CopyMatrix
        NextStepMatrix
        NextStepMatrixSize
        Log
    end
    
    methods
        function obj = Conway4D(matrix)
            bin_matrix = matrix == '#';
            obj.Matrix = bin_matrix;
            obj.MatrixSize = [size(matrix, 1), size(matrix, 2), size(matrix, 3), size(matrix, 4)];
            obj.NextStepMatrix = obj.create_next_step_matrix();
            obj.NextStepMatrixSize = size(obj.NextStepMatrix);
            obj.CopyMatrix = obj.create_copy_matrix();
            
        end
        
        
        function nsm = create_next_step_matrix(obj)
            nsm = false(obj.MatrixSize +2);
        end
        
        function cm = create_copy_matrix(obj)
            cm = obj.create_next_step_matrix();
            cm(2:end-1, 2:end-1, 2:end-1, 2:end-1) = obj.Matrix;
        end

        
        function status = find_status(obj,suby,subx,subz,subw)
            if obj.CopyMatrix(suby,subx,subz,subw)
                if any(obj.neighbour_count(suby,subx,subz,subw) == [2,3])
                    status = 1;
                else
                    status = 0;
                end
            else
                if obj.neighbour_count(suby,subx,subz,subw) == 3
                    status = 1;
                else
                    status = 0;
                end
            end
        end
                
         
        function n = neighbour_count(obj, suby, subx, subz,subw)
            ys = (max(1,suby-1):min(suby+1,obj.NextStepMatrixSize(1)));
            xs = (max(1,subx-1):min(subx+1,obj.NextStepMatrixSize(2)));
            zs = (max(1,subz-1):min(subz+1,obj.NextStepMatrixSize(3)));
            ws = (max(1,subw-1):min(subw+1,obj.NextStepMatrixSize(4)));
            n = sum(obj.CopyMatrix(ys,xs, zs,ws),'all')-obj.CopyMatrix(suby,subx,subz,subw);
        end
        
        function obj = update(obj,n)
            obj.Log = struct();
            %update n times
            for i = 1:n
                obj.Log.sum(i) = obj.sum_of_active_elements();
                obj.Log.mean(i) = obj.density();
                index_range = 1:numel(obj.CopyMatrix);
                [ys,xs,zs,ws] = arrayfun(@(idx) ind2sub(obj.NextStepMatrixSize, idx), index_range);
                new_vals = arrayfun(@(idx) obj.find_status(ys(idx),xs(idx),zs(idx),ws(idx)), index_range);
                obj.NextStepMatrix(index_range) = new_vals;
                obj.Matrix = obj.NextStepMatrix;
                obj.MatrixSize = size(obj.Matrix);
                obj.NextStepMatrix = obj.create_next_step_matrix();
                obj.NextStepMatrixSize = size(obj.NextStepMatrix);
                obj.CopyMatrix = obj.create_copy_matrix();
            end
            obj.Log.sum(n+1) = obj.sum_of_active_elements();
            obj.Log.mean(n+1) = obj.density();
        end
        
        function res = sum_of_active_elements(obj)
            res = sum(obj.Matrix, "all");
        end
        
        function res = density(obj)
            res = mean(obj.Matrix, "all");
        end
    end
end